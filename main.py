from flask import Flask, request, render_template, jsonify

from utils import load_data, prepare_posts

posts, comments, bookmarks = load_data()

posts = prepare_posts(posts, comments)

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False


@app.route('/')
def page_index():
    return render_template("index.html", posts=posts, comments=comments)


@app.route('/posts/<int:post_id>')
def page_current_post(post_id):
    for post in posts:
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
    user_posts = []
    for post in posts:
        if post["poster_name"] == username:
            user_posts.append(post)

    return render_template("user-feed.html", posts=user_posts)


@app.route('/api/posts')
def get_api_posts():
    return jsonify(posts), 200


@app.route('/api/posts/<int:post_id>')
def get_api_post(post_id):
    if post_id <= len(posts):
        return jsonify(posts[post_id - 1]), 200
    return 'not found', 404


app.run()
