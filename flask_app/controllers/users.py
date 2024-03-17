from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect("/")
    User.save(request.form)
    return redirect("/users")


@app.route("/users")
def show_users():
    users = User.get_all()

    return render_template("users.html", all_users=users)


@app.route("/show_user/<int:user_id>")
def user(user_id):
    user = User.one_user({"id": user_id})
    return render_template("single_user.html", user=user)


@app.route("/update_user/<int:user_id>")
def edit_user(user_id):
    user = User.one_user({"id": user_id})
    return render_template("edit_user.html", user=user)


@app.route("/change_user/<int:user_id>", methods=["POST"])
def update_user(user_id):
    data = {
        "id": user_id,
        "first_name": request.form["fname"],
        "last_name": request.form["lname"],
        "email": request.form["email"],
    }

    User.update(data)
    return redirect("/users")


@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    User.delete({"id": user_id})
    return redirect("/users")
