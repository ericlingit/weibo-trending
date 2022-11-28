# Weibo trending posts scraper

Scrap trending posts from Weibo front page.

<!--
For notes detailing Weibo API endpoints and their responses, see the wiki:
https://github.com/ericlingit/weibo-trending/wiki/Weibo-API
-->

## Usage guide

### As a library

Install

`pip install weibo-trending`

Get and parse posts

```python
from weibo_trending import get_new_posts, parse_response

resp = get_new_posts()
mblogs = parse_response(resp)
for mblog in mblogs:
    print(mblog)
```

### As a command line tool

Install

`pip install weibo-trending`

Usage

```
python -m weibo_trending --help

    usage: weibo_trending [-h] [-d DIR] [-s]

    Scrape and parse Weibo trending posts.

    optional arguments:
    -h, --help          show this help message and exit
    -d DIR, --dir DIR   specify the output directory. Defaults to the current working directory
    -s, --skip-parsing  whether to skip parsing and dump the raw JSON response from Weibo


python -m weibo_trending
```

weibo_trending will save each scraped post with the following filename format:
- `weibo_<user ID>_<post ID>.json`
- Example: `weibo_1631153043_4834313265233660.json`

Each call to weibo_trending usually saves 10 new files. If you get fewer than 10, that means the response contains one or more deleted posts. They are not saved.

## Develop

```
git clone https://github.com/ericlingit/weibo-trending.git
cd weibo-trending
python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
pip install -e .
pytest
```

### Package

```
python -m build --wheel
```

The built wheel is in `./dist/`.
