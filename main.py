from flask import Flask, request, render_template

from utils import load_data, prepare_posts

posts, comments, bookmarks = load_data()

posts = prepare_posts(posts, comments)

app = Flask(__name__)


@app.route('/')
def page_index():
    return render_template("index.html", posts=posts, comments=comments)


@app.route('/posts/<post_id>')
def page_current_post(post_id):
    i = 0
    for post in posts:
        i += 1
        if post["pk"] == int(post_id):
            return render_template("post.html", comments=post['comments'], post=post)
    return 'not found', 404


@app.route('/search/', methods=['POST', 'GET'])
def search_post():
    s = request.args.get('s')
    found_posts = []
    if s:
        for post in posts:
            if s in post['content']:
                found_posts.append(post)

    return render_template("search.html", posts=found_posts)


@app.route('/users/<username>')
def all_user_posts(username):
    for post in posts:
        if post["poster_name"] == username:
            return render_template("user-feed.html", post=post)
    return 'not found', 404


app.run()
