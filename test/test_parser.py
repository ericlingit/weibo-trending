import json

from weibo_trending import parse_comments, parse_response


def test_parse_posts():
    with open("test/response.json") as fh:
        data: dict = json.load(fh)
    mblogs = parse_response(data)

    # One of the mblogs has been deleted, so the total number of mblogs should be 9, not 10.
    assert len(mblogs) == 9


def test_parse_comments():
    with open("test/comments.json") as fh:
        data: dict = json.load(fh)
    raw_comments = data.get("data", {}).get("data", [])

    comments = parse_comments(raw_comments)
    assert len(comments) == 20

    with open("test/comment-with-replies.json") as fh:
        data: dict = json.load(fh)
    raw_comments = data.get("data", {}).get("data", [])

    comments = parse_comments(raw_comments)
    assert len(comments) == 20
    assert len(comments[0].comments) == 2
    assert len(comments[0].comments[0].comments) == 0
