from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required

from ..app import app
from ..models.entries import Entry


def numbering():
    for i in range(0, 5):
        yield i


@app.route("/")
@login_required
def show_entries():
    it = Entry.scan()
    entries = sorted(it, key=lambda x: x.id, reverse=True)
    return render_template("entries/index.html", entries=entries)


@app.route("/entries", methods=["POST"])
@login_required
def add_entry():
    entry = Entry(
        id=int(datetime.now().timestamp()),
        title=request.form["title"],
        text=request.form["text"],
    )
    entry.save()
    flash("新しい記事が作成されました")
    return redirect(url_for("show_entries"))


@app.route("/entries/new", methods=["GET"])
@login_required
def new_entry():
    return render_template("entries/new.html")


@app.route("/entries/<int:id>", methods=["GET"])
@login_required
def show_entry(id):
    entry = Entry.get(id)
    return render_template("entries/show.html", entry=entry)


@app.route("/entries/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry(id):
    entry = Entry.get(id)
    return render_template("entries/edit.html", entry=entry)


@app.route("/entries/<int:id>/update", methods=["POST"])
@login_required
def update_entry(id):
    entry = Entry.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    entry.save()
    flash("記事が更新されました")
    return redirect(url_for("show_entries"))


@app.route("/entries/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry(id):
    entry = Entry.get(id)
    entry.delete()
    flash("記事が削除されました")
    return redirect(url_for("show_entries"))
