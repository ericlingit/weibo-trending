from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

request_url = "https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0"
request_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "MWeibo-Pwa": "1",
    "Connection": "keep-alive",
    "Referer": "https://m.weibo.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers",
}


def get_new_posts() -> dict:
    """Get new posts from Weibo, and return the rawo JSON response.
    A successful response contains 10 new posts.
    """
    resp = requests.get(url=request_url, headers=request_headers)
    resp.raise_for_status()
    return resp.json()


@dataclass
class User:
    id: int
    profile_url: str
    screen_name: str
    gender: str
    followers_count: str  # Example: "433.8万".


@dataclass
class Microblog:
    text: str
    id: str
    url: str
    poster: User
    pics: List[str]
    created_at: str
    source: str  # `source` is the device used to create the post.


def parse_response(data: dict) -> List[Microblog]:
    """Parse the raw JSON response from Weibo."""
    posts: List[Microblog] = []
    for card in data["data"]["cards"]:
        mb: Optional[dict] = card["mblog"]
        if not mb:
            # print(f"no content in card: {card}")
            continue

        post_raw_content = mb["text"]
        post_text = BeautifulSoup(post_raw_content, "lxml").text

        u = mb.get("user")
        if u is None:
            # Post has been deleted.
            continue

        user = User(
            id=mb.get("user", {}).get("id", -1),
            screen_name=mb.get("user", {}).get("screen_name", ""),
            profile_url=mb.get("user", {}).get("profile_url", ""),
            gender=mb.get("user", {}).get("gender", "?"),
            followers_count=mb.get("user", {}).get("followers_count", ""),
        )

        # Extract pic URLs, if any.
        pics: List[str] = []
        if mb.get("pic_num", 0) != 0:
            for item in mb.get("pics", [{}]):
                pic_url = item.get("url", "")
                if pic_url:
                    pics.append(pic_url)

        post = Microblog(
            id=mb.get("id", ""),
            created_at=mb.get("created_at", ""),
            text=post_text,
            source=mb.get("source", ""),
            poster=user,
            url=f"https://m.weibo.cn/status/{mb['id']}",
            pics=pics,
        )
        posts.append(post)
    return posts
