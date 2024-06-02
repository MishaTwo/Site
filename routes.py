import os
from models.base import session
from models.post import Post
from app import app
from flask import render_template, request, redirect
from dotenv import load_dotenv


load_dotenv()

@app.route("/")
def all():
    posts = session.query(Post).all()
    return render_template("index.html", posts=posts)

@app.route("/read/<int:id>")
def read(id):
    post = session.query(Post).get(id)
    return render_template("read_detail.html", post=post)

@app.route("/delete/<int:id>")
def delete(id):
    post = session.query(Post).filter_by(id=id).first()
    if post:
        session.delete(post)
        session.commit()
    session.close()
    return redirect("/")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        create_post = Post(
            title=title,
            content=content
        )

        try:
            session.add(create_post)
            session.commit()
            return redirect('/')
        except Exception as exc:
            return f"При створюванні виникла помилка {exc}!"
        finally:
            session.close()
    else:
        return render_template("create.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = session.query(Post).get(id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        create_post = Post(
            title=title,
            content=content
        )

        session.commit()
        session.close()
        return redirect("/")
    else:
        return render_template("edit.html", post=post)