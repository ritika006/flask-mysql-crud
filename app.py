from flask import Flask, render_template, request, redirect, url_for
from models import db, User
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/") # READ
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/add", methods=["GET", "POST"]) # CREATE
def add():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"]) # UPDATE
def edit(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", user=user)


@app.route("/delete/<int:id>") # DELETE
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
