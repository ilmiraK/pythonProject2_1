import json


def load_data():
    with open("data/data.json", "r") as fp:
        posts = json.load(fp)

    with open("data/comments.json", "r") as fp:
        comments = json.load(fp)
    posts = prepare_posts(posts, comments)
    with open("data/bookmarks.json", "r") as fp:
        bookmarks = json.load(fp)

    return posts, comments, bookmarks


def prepare_posts(posts, comments):
    for i, post in enumerate(posts):
        pk = post.get("pk")
        post_comments = []
        for comment in comments:
            if comment.get("post_id") == pk:
                post_comments.append(comment)
        posts[i]["comment"] = post_comments
        posts[i]["comment_count"] = len(post_comments)
        posts[i]["content"] = tag_content(posts[i]["content"])
    return posts


def tag_content(content):
    words = content.split(' ')
    for i, word in enumerate(words):
        if word.startswith('#'):
            tag = word.replace('#', '')
            link = f"<a href='/tag/{tag}'>{word}</a>"
            words[i] = link

    return " ".join(words)
