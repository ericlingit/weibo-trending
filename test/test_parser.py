import json

from weibo_trending import parse_posts


def test_parse_posts():
    with open("test/response.json") as fh:
        data: dict = json.load(fh)
    posts = parse_posts(data)

    assert len(posts) > 0
