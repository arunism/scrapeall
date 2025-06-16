import argparse
import asyncio

from tqdm import tqdm

from scrapeall.parse import HTMLParser
from scrapeall.utils import ProcessMode, save_data


async def main(
    vendor: str, config_path: str, MODE: ProcessMode, output_file: str = ""
) -> dict:
    data = dict()

    parser = HTMLParser(vendor, config_path, MODE)
    await parser.initialize_browser()
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data

    await parser.close_browser()
    if output_file:
        await save_data(filename=output_file, data=data)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the processing with vendor, config, and optional mode/output."
    )
    parser.add_argument("--vendor", required=True, help="Your vendor name (required)")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to your YAML configuration file (required)",
    )
    parser.add_argument(
        "--mode",
        choices=[m.value for m in ProcessMode],
        default="both",
        help="Processing mode (default: both)",
    )
    parser.add_argument(
        "--output", default="output.json", help="Output filename (default: output.json)"
    )

    args = parser.parse_args()

    mode = ProcessMode(args.mode)

    data = asyncio.run(main(args.vendor, args.config, mode, args.output))
