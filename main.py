from flask import Flask
from flask import request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello {escape(name)}!"

@app.route("/post/<int:post_id>")
def post(post_id):
    return f"Post {escape(post_id)}!"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Path {escape(subpath)}!"

@app.route("/projects/")
def projects():
    return "The projects page"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "POST LOGIN"
    else:
        return "GET LOGIN"
    
@app.route("/bye/")
@app.route("/bye/<name>")
def bye(name=None):
    return render_template("bye.html", name=name)