import asyncio
from itertools import chain
from omegaconf import OmegaConf
from pyppeteer import launch
from bs4 import BeautifulSoup


config = OmegaConf.load("config.yaml")


class HTMLParser:
    def __init__(self, vendor: str) -> None:
        self.config = config[vendor].to_dict()
        self.browser = None
        self.page = None
        self.urls = dict()

    async def initialize_browser(self):
        self.browser = await launch(headless=True, args=["--no-sandbox"])

    async def close_browser(self) -> None:
        if self.browser:
            await self.browser.close()

    async def get_page(self, url: str):
        page = await self.browser.newPage()
        await page.goto(url)
        content = await page.content()
        self.page = BeautifulSoup(content, "html.parser")

    async def get_all_urls(self, url: str = None):
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
                if "https" not in link:
                    link = "https://www.masta-travel-health.com/" + link
                self.urls[text] = link
