# Web Scraper for Static and JS Rendered Sites

This repository contains a versatile web scraper capable of handling both statically rendered HTML sites and dynamically rendered JavaScript sites. By combining techniques for traditional HTML scraping with methods for interacting with JavaScript-heavy websites, this single program offers a comprehensive solution for extracting data from a wide range of web sources.

## Features

- **Dual Scraping Modes:** Can processes static HTML or JS-rendered content.
- **Headless Browser Support:** Utilizes headless browsers to render and scrape JavaScript-heavy sites.
- **Easy Configuration:** Simple setup and configuration to specify target URLs and data extraction rules.
- **Efficient Data Extraction:** Optimized for speed and reliability, ensuring accurate data retrieval.
<!-- Extensive Logging: Provides detailed logs for monitoring scraping activities and troubleshooting. -->

## Usage

### 1. Modify the `config.yaml` file as per your requirement.

- The configuration should follow same format as shown in `config.yaml` by default as a sample.
- The `terminator` key in configuration is optional. Only required if you have a specific terminating point to stop scraping.
- The `path` key can have multiple values, in case you want to extract elements from multiple css-selectors.
- The depth of configuration does not matter as long as the depth ends with the key `path`.

Here's the sample configuration for you:

```yaml
<YOUR_VENDOR_NAME>:
  base:
    url: <URL_OF_THE_SITE_FROM-WHERE_YOU_WANT_TO_EXTRACT_ALL_URLS>
    path:
      - <PATH_TO_SINGLE_URL_ELEMENT>
  content:
    <CONTENT_SECTION_1>:
      path:
        - <YOUR_CSS_SELECTOR_PATH>
      terminator: <YOUR_CSS_SELECTOR_PATH_TO_TERMINATING_POINT>
    <CONTENT_SECTION_2>:
      path:
        - <YOUR_CSS_SELECTOR_PATH>
      terminator: <YOUR_CSS_SELECTOR_PATH_TO_TERMINATING_POINT>
```

### 2. Run the following code

To get the JS-Rendered Content using Headless browser, follow along with the code below:

```python
import asyncio

from tqdm import tqdm


async def main(vendor: str, config_path: str):
    data = dict()

    parser = HTMLParser(vendor, config_path)
    await parser.initialize_browser()
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data

    await parser.close_browser()
    return data


if __name__ == "__main__":
    VENDOR = "<YOUR_VENDOR_NAME>"
    CONFIG_PATH = "<PATH_TO_YOUR_YAML_FILE>"
    data = asyncio.run(main(VENDOR, CONFIG_PATH))
```

To get the Content from static HTML sites/pages, modify the main function as follows:

```python
async def main(vendor: str, config_path: str):
    data = dict()

    parser = HTMLParser(vendor, config_path)
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data
    return data
```

If you want to save the content scrapped, you can do that by following the given code snippet:

```python
import asyncio

from tqdm import tqdm

from utils import save_data
from parse import HTMLParser


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


if __name__ == "__main__":
    VENDOR = "<YOUR_VENDOR_NAME>"
    CONFIG_PATH = "<PATH_TO_YOUR_YAML_FILE>"
    OUTPUT_FILE = "<PATH_TO_YOUR_JSON_FILE>"
    data = asyncio.run(main(VENDOR, CONFIG, OUTPUT_FILE))
```

> Remember: **YOUR_VENDOR_NAME** should match one in the **<CONFIG_PATH>.yaml** file.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.
