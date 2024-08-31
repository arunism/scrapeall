from setuptools import find_packages, setup


with open("README.md", "r") as file:
    long_desc = file.read()


setup(
    name="scrapeall",
    version="0.1.2",
    description="Versatile web scraper for extracting data from both static HTML and JavaScript-rendered sites, using headless browsers for dynamic content.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    # package_dir={"": "scrapeall"},
    packages=find_packages(),
    url="https://github.com/arunism/scrapeall",
    author="Arun Ghimire",
    author_email="thearunism@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyppeteer==2.0.0",
        "beautifulsoup4==4.12.3",
        "requests==2.32.3",
        "omegaconf==2.3.0",
    ],
    # extras_require={
    #     "dev": ["setuptools>=74.0.0", "wheel>=0.44.0", "twine>=5.1.1"],
    # },
    python_requires=">=3.10",
)
