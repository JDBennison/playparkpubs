import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
@app.route("/index")
def index():
    most_recent = mongo.db.reviews.find().limit(10).sort("_id", -1)
    reviews = mongo.db.reviews.find().sort("_id", -1)
    return render_template("index.html", most_recent=most_recent, reviews=reviews)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password is correct
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome {}".format(
                        request.form.get("username").capitalize()))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesnt exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/read_review/<review_id>", methods=["GET", "POST"])
def read_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("read_review.html", review=review)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        ratings = [int(request.form.get("service")), int(request.form.get("atmosphere")), int(request.form.get("food")), int(request.form.get("value")), int(request.form.get("park"))]
        total_score = round(((sum(ratings)) * 0.4), 1)
        review = {
            "pub_name": request.form.get("pub_name"),
            "pub_address": request.form.get("pub_address"),
            "website": request.form.get("website"),
            "phone_number": request.form.get("phone_number"),
            "review_headline": request.form.get("review_headline"),
            "review_adult": request.form.get("review_adult"),
            "review_kids": request.form.get("review_kids"),
            "service": request.form.get("service"),
            "atmosphere": request.form.get("atmosphere"),
            "food": request.form.get("food"),
            "value": request.form.get("value"),
            "park": request.form.get("park"),
            "total_score": total_score,
            "review_date": request.form.get("review_date"),
            "category_name": request.form.getlist("category_name"),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(review)
        flash("Review Successfully Added")
        return redirect(url_for("index"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_review.html", categories=categories)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":
        ratings = [int(request.form.get("service")), int(request.form.get("atmosphere")), int(request.form.get("food")), int(request.form.get("value")), int(request.form.get("park"))]
        total_score = round(((sum(ratings)) * 0.4), 1)
        submit = {
            "pub_name": request.form.get("pub_name"),
            "pub_address": request.form.get("pub_address"),
            "website": request.form.get("website"),
            "phone_number": request.form.get("phone_number"),
            "review_headline": request.form.get("review_headline"),
            "review_adult": request.form.get("review_adult"),
            "review_kids": request.form.get("review_kids"),
            "service": request.form.get("service"),
            "atmosphere": request.form.get("atmosphere"),
            "food": request.form.get("food"),
            "value": request.form.get("value"),
            "park": request.form.get("park"),
            "total_score": total_score,
            "review_date": request.form.get("review_date"),
            "category_name": request.form.getlist("category_name"),
            "created_by": session["user"]
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")
        return redirect(url_for('read_review', review_id=ObjectId(review_id)))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_review.html", review=review, categories=categories)

@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfully Deleted")
    return redirect(url_for("index"))

@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))
        
    return render_template("add_category.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")), debug=True)