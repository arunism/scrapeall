from pyppeteer import launch
from omegaconf import OmegaConf


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