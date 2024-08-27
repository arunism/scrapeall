import asyncio

from tqdm import tqdm

from scrapeall.utils import save_data
from scrapeall.parse import HTMLParser


async def main(vendor: str, config_path: str, output_file: str = ""):
    data = dict()

    parser = HTMLParser(vendor, config_path)
    await parser.initialize_browser()
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data

    await parser.close_browser()
    if output_file:
        await save_data(filename=output_file, data=data)
    return data
