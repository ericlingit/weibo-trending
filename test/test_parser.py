import json

from weibo_trending import parse_response


def test_parse_posts():
    with open("test/response.json") as fh:
        data: dict = json.load(fh)
    mblogs = parse_response(data)

    # One of the mblogs has been deleted, so the total number of mblogs should be 9, not 10.
    assert len(mblogs) == 9
