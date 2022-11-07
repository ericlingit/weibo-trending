from typing import List

import requests
from bs4 import BeautifulSoup

URL = "https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
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
    # Each request returns 10 new posts.
    resp = requests.get(url=URL, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def parse_new_posts(data: dict) -> List[dict]:
    posts: List[dict] = []
    for card in data["data"]["cards"]:
        mb = card["mblog"]

        post_raw_content = mb["text"]
        post_text = BeautifulSoup(post_raw_content, "lxml").text

        post = {
            "post_id": mb["id"],
            "post_text": post_text,
            "post_pics": mb["pic_ids"],
            "user_id": mb["user"]["id"],
            "user_screen_name": mb["user"]["screen_name"],
            "user_profile_url": mb["user"]["profile_url"],
            "user_gender": "female" if mb["user"]["gender"] == "f" else "male",
            "user_followers_count": mb["user"]["followers_count"],
        }
        posts.append(post)
    return posts
