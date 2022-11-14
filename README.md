# Weibo trending posts scraper

Scrap trending posts from Weibo front page.


## Weibo API

To understand how Weibo fetches new posts, a network inspection is performed on the mobile website.

A request to this API endpoint is observed: `https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0`


![Screenshot of content API request](./img/inspect-api-url.png)

Its response looks like this:

![Screenshot of content API response](./img/inspect-response-cards.png)

The response is a nested JSON object. We're interested in the items in `data`'s `cards` array.

Each *card* contains a `mblog` (microblog) object that encapsulates the content as well as metadata about the content.

One call to the API returns ten cards. When the device viewport scrolls toward the bottom of the page, the API is called again to fetch 10 more posts.

weibo-trending extracts the following fields from `mblog`:
- `text`: post text; can contain HTML tags when a video stream is included
- `id`: post ID (str)
- `url`: link to the post
- `user`: the poster
- `pics`: the URLs to the images included in this post (array of objects)
- `created_at`: post date (str)
- `source`: the device the post is submitted from

In addition, the following `user` fields are also extracted:
- `id`: user ID (int)
- `profile_url`: link to user profile
- `screen_name`: screen name
- `gender`: `"f"` for female, `"m"` for male. Weibo does not provide codes for those who are non-binary
- `followers_count`: the str number of followers in units of 10,000. For example: `"433.8万"` (4,338,000).

Note that repeated calls sometimes return posts that have been returned before.


## weibo-trending usage guide

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

### Packaging

```
python -m build --wheel
```

The built wheel is in `./dist/`.
