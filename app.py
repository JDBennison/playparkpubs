import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
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

cloudinary.config( 
  cloud_name = os.environ.get("CLOUD_NAME"), 
  api_key = os.environ.get("API_KEY"), 
  api_secret = os.environ.get("API_SECRET")
)

mongo = PyMongo(app)

@app.route("/")
@app.route("/index")
def index():
    most_recent = mongo.db.reviews.find().limit(10).sort("_id", -1)
    reviews = mongo.db.reviews.find().sort("_id", -1)
    return render_template("index.html", most_recent=most_recent, reviews=reviews)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    most_recent = mongo.db.reviews.find().limit(10).sort("_id", -1)
    reviews = mongo.db.reviews.find({"$text": {"$search": query}})
    return render_template("index.html", most_recent=most_recent, reviews=reviews)

@app.route("/sort", methods=["GET", "POST"])
def sort():
    sort_by = request.form.get("sort_by")
    most_recent = mongo.db.reviews.find().limit(10).sort("_id", -1)
    if sort_by == "az":
        reviews = mongo.db.reviews.find().sort("pub_name", 1)
    elif sort_by == "za":
        reviews = mongo.db.reviews.find().sort("pub_name", -1)
    elif sort_by == "dateasc":
        reviews = mongo.db.reviews.find().sort("_id", 1)
    elif sort_by == "datedesc":
        reviews = mongo.db.reviews.find().sort("_id", -1)
    elif sort_by == "highestrated":
        reviews = mongo.db.reviews.find().sort("total_score", -1)
    else:
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
    reviews = mongo.db.reviews.find({"created_by": session["user"]})
    return render_template("profile.html", username=username, reviews=reviews)

@app.route("/review_by_category/<category_id>")
def review_by_category(category_id):
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    reviews = []
    for review in mongo.db.reviews.find():
        if category_id in review["category_list"]:
            reviews.append(review)
    print(category)
    return render_template("review_by_category.html", category=category, reviews=reviews)


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/read_review/<review_id>", methods=["GET", "POST"])
def read_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    categories = []
    for ident in review["category_list"]:
        category = mongo.db.categories.find_one({"_id": ObjectId(ident)})
        categories.append(category)
    return render_template("read_review.html", review=review, categories=categories)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        ratings = [int(request.form.get("service")), int(request.form.get("atmosphere")), int(request.form.get("food")), int(request.form.get("value")), int(request.form.get("park"))]
        total_score = round(((sum(ratings)) * 0.4), 1)
        photo = request.files['photo_url']
        photo_upload = cloudinary.uploader.upload(photo)
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
            "category_list": request.form.getlist("category_list"),
            "created_by": session["user"],
            "photo_url": photo_upload["secure_url"]
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
        if request.form.get("file_name") != mongo.db.reviews.find_one({"_id": ObjectId(review_id)})["photo_url"]: 
            photo = request.files['photo_url']
            photo_upload = cloudinary.uploader.upload(photo)
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
                "category_list": request.form.getlist("category_list"),
                "created_by": session["user"],
                "photo_url": photo_upload["secure_url"]
            }
            mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
            flash("Review Successfully Updated")
            return redirect(url_for('read_review', review_id=ObjectId(review_id)))
        else:
            photo_url = request.form.get("file_name")
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
                "category_list": request.form.getlist("category_list"),
                "created_by": session["user"],
                "photo_url": photo_url
            }
            mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
            flash("Review Successfully Updated")
            return redirect(url_for('read_review', review_id=ObjectId(review_id)))


    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    prefilled_categories = []
    for ident in review["category_list"]:
        category = mongo.db.categories.find_one({"_id": ObjectId(ident)})
        prefilled_categories.append(category)
    
    return render_template("edit_review.html", review=review, categories=categories, prefilled_categories=prefilled_categories)

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


@app.route("/edit_category/<category_id>", methods=["GET", "POST"] )
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories"))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")), debug=True)