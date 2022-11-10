from . import get_new_posts, parse_posts


def main() -> None:
    """
    Options:
    - save .json files to dir. pwd if not specified.
    - skip parsing and dump raw json
    """
    data = get_new_posts()
    posts = parse_posts(data)
    print(posts)


if __name__ == "__main__":
    main()
