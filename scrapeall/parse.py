import os
from itertools import chain
from typing import Dict, Union
from urllib.parse import urljoin, urlparse

import httpx
import requests
from bs4 import BeautifulSoup
from omegaconf import OmegaConf
from pyppeteer import launch

from scrapeall.utils import ProcessMode


class HTMLParser:
    def __init__(self, vendor: str, config_path: str, mode: ProcessMode) -> None:
        config = OmegaConf.load(config_path)
        self.config = OmegaConf.to_container(config[vendor], resolve=True)
        self.browser = None
        self.page = None
        self.urls: dict = {}
        self.mode = mode

    async def initialize_browser(self) -> None:
        self.browser = await launch(headless=True, args=["--no-sandbox"])

    async def close_browser(self) -> None:
        if self.browser:
            await self.browser.close()

    async def get_page(self, url: str):
        if self.browser:
            page = await self.browser.newPage()
            await page.goto(url)
            content = await page.content()
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
            else:
                response.raise_for_status()
        self.page = BeautifulSoup(content, "html.parser")

    async def get_all_urls(self, url: str = None, base_url: str = None):
        elements = list()
        url = url or str(self.config["base"]["url"])
        await self.get_page(url)
        elements.extend(
            chain.from_iterable(
                self.page.select(path) for path in self.config["base"]["path"]
            )
        )
        for element in elements:
            text = element.text.strip()
            link = element.get("href")
            if text and link:
                if not link.startswith("http"):
                    base_url = (
                        base_url
                        or urlparse(self.config["base"]["url"])
                        ._replace(path="")
                        .geturl()
                    )
                link = urljoin(base_url, link)
                self.urls[text] = link

    async def download_file(self, url: str, filename: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
                with open(filename, "wb") as f:
                    f.write(response.content)
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

    async def get_page_content(
        self, url: str, config: Dict[str, Union[list, str, dict]]
    ):
        if "path" in config:
            data = ""
            for path in config.get("path"):
                if path and config.get("terminator"):
                    element = self.page.select_one(path)
                    terminating_element = self.page.select_one(config.get("terminator"))
                    while element:
                        if element == terminating_element:
                            break
                        if (
                            self.mode == ProcessMode.URLS_ONLY
                            or self.mode == ProcessMode.BOTH
                        ):
                            href = element.get("href")
                            if href:
                                if not href.startswith("http"):
                                    link = urljoin(url, href)
                                else:
                                    link = href

                                # filename = href.replace("/", "-")
                                success = await self.download_file(link, href)
                                if success:
                                    print(f"Downloaded: {href}")
                                    if self.mode == ProcessMode.URLS_ONLY:
                                        continue
                        if (
                            self.mode == ProcessMode.TEXT_ONLY
                            or self.mode == ProcessMode.BOTH
                        ):
                            data += "\n\n" + element.text.strip()
                        element = element.find_next()

                elif path and not config.get("terminator"):
                    for element in self.page.select(path):
                        if (
                            self.mode == ProcessMode.URLS_ONLY
                            or self.mode == ProcessMode.BOTH
                        ):
                            href = element.get("href")
                            if href:
                                if not href.startswith("http"):
                                    link = urljoin(url, href)
                                else:
                                    link = href

                                # filename = href.replace("/", "-")
                                success = await self.download_file(link, href)
                                if success:
                                    print(f"Downloaded: {href}")
                                    if self.mode == ProcessMode.URLS_ONLY:
                                        continue
                        if (
                            self.mode == ProcessMode.TEXT_ONLY
                            or self.mode == ProcessMode.BOTH
                        ):
                            data += "\n\n" + element.text.strip()
            return data.strip()
        data = {}
        for key, value in config.items():
            data[key] = await self.get_page_content(url, value)
        return data

    async def get_content(self, url: str):
        self.data = {}
        await self.get_page(url)
        for key, value in self.config.get("content").items():
            self.data[key] = await self.get_page_content(url, value)
