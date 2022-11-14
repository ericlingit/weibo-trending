import argparse
import json
import sys
from pathlib import Path

from . import get_new_posts, parse_response


def main() -> None:
    """
    Options:
    - Save JSON files to dir; pwd if not specified.
    - Skip parsing and dump raw JSON response from Weibo.
    """
    parser = argparse.ArgumentParser(
        prog="weibo_trending",
        description="Scrape and parse Weibo trending posts.",
    )
    # Output dir.
    parser.add_argument(
        "-d",
        "--dir",
        action="store",
        default=".",
        required=False,
        help="specify the output directory. Defaults to the current working directory",
    )
    # Skip parsing and dump raw response JSON.
    parser.add_argument(
        "-s",
        "--skip-parsing",
        action="store_true",
        required=False,
        help="whether to skip parsing and dump the raw JSON response from Weibo",
    )
    args = parser.parse_args()

    out_dir = Path(getattr(args, "dir", ".")).resolve()
    if not out_dir.is_dir():
        sys.exit(f"error: not a directory: {out_dir.as_posix()}")
    skip_parsing: bool = getattr(args, "skip_parsing", False)

    resp = get_new_posts()
    if skip_parsing:
        with (out_dir / "weibo_response.json").open("w") as f_resp:
            json.dump(resp, f_resp, ensure_ascii=False, indent=4)
        return
    mblogs = parse_response(resp)
    for mb in mblogs:
        with (out_dir / f"weibo_{mb.poster.id}_{mb.id}.json").open("w") as f_mb:
            json.dump(mb.to_dict(), f_mb, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
