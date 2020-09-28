"""
This module is designed for play park pubs, a review app which will take
inputted reviews, stored in MongoDB and display them for possible consumers
"""
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
from flask_paginate import Pagination, get_page_args
if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    """Main page which shows all reviews, the last ten reviewed pubs and is paginated"""
    most_recent = mongo.db.reviews.find().limit(10).sort('_id', -1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = mongo.db.reviews.find().count()
    thereviews = mongo.db.reviews.find().sort('_id', -1)
    paginated_reviews = thereviews[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materialize')
    return render_template('index.html',
                           reviews=paginated_reviews,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           most_recent=most_recent
                           )

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Lets users search reviews by address, name or content of review"""
    query = request.form.get('query')
    most_recent = mongo.db.reviews.find().limit(10).sort('_id', -1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = mongo.db.reviews.find({'$text': {'$search': query}}).count()
    thereviews = mongo.db.reviews.find({'$text': {'$search': query}})
    paginated_reviews = thereviews[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materialize')
    return render_template('index.html',
                           reviews=paginated_reviews,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           most_recent=most_recent
                           )

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    """Lets users view the different reviews sorted in various ways"""
    sort_by = request.form.get('sort_by')
    most_recent = mongo.db.reviews.find().limit(10).sort('_id', -1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = mongo.db.reviews.find().count()
    if sort_by == 'az':
        thereviews = mongo.db.reviews.find().sort('pub_name', 1)
    elif sort_by == 'za':
        thereviews = mongo.db.reviews.find().sort('pub_name', -1)
    elif sort_by == 'dateasc':
        thereviews = mongo.db.reviews.find().sort('_id', 1)
    elif sort_by == 'datedesc':
        thereviews = mongo.db.reviews.find().sort('_id', -1)
    elif sort_by == 'highestrated':
        thereviews = mongo.db.reviews.find().sort('total_score', -1)
    else:
        thereviews = mongo.db.reviews.find().sort('_id', -1)
    paginated_reviews = thereviews[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materialize')
    return render_template('index.html',
                           reviews=paginated_reviews,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           most_recent=most_recent
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Lets a new user register to write reviews"""
    if request.method == 'POST':
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        new_user = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password'))
        }
        mongo.db.users.insert_one(new_user)

        # put the new user into session cookie
        session['user'] = request.form.get('username').lower()
        flash('Registration Successful')
        return redirect(url_for('profile', username=session['user']))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in user and checks password
    """
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            if check_password_hash(
                    existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                flash('Welcome {}'.format(
                    request.form.get('username').capitalize()))
                return redirect(url_for('profile', username=session['user']))
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))
        flash('Incorrect Username and/or Password')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/profile/<username>')
def profile(username):
    """
    Grabs the session user's username from db and also all the reviews written by that user
    """
    username = mongo.db.users.find_one(
        {'username': session['user']})['username']
    reviews = mongo.db.reviews.find({'created_by': session['user']})
    return render_template('profile.html', username=username, reviews=reviews)

@app.route('/review_by_category/<category_id>')
def review_by_category(category_id):
    """
    Displays all the reviews from a category. Also inserted pagination
    """
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    reviews = []
    for review in mongo.db.reviews.find():
        if category_id in review['category_list']:
            reviews.append(review)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(reviews)
    paginated_reviews = reviews[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materialize')
    return render_template('review_by_category.html',
                           reviews=paginated_reviews,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           category=category
                           )


@app.route('/logout')
def logout():
    """
    Logs a user out by removing user from session cookies
    """
    flash('You have been logged out')
    session.pop("user")
    return redirect(url_for('login'))


@app.route('/read_review/<review_id>', methods=['GET', 'POST'])
def read_review(review_id):
    """
    This displays all the data for one individual review. It also makes sure it
    takes the categories it has connected to.
    """
    review = mongo.db.reviews.find_one({'_id': ObjectId(review_id)})
    categories = []
    for ident in review['category_list']:
        category = mongo.db.categories.find_one({'_id': ObjectId(ident)})
        categories.append(category)
    return render_template('read_review.html', review=review, categories=categories)


@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    """
    This allows a user to submit a review. It takes all the elements from
    the input form and also works out what the overall rating would be
    as well as automatically cropping the photo so that it is a square.
    """
    if request.method == 'POST':
        ratings = [int(request.form.get('service')),
                   int(request.form.get('atmosphere')),
                   int(request.form.get('food')),
                   int(request.form.get('value')),
                   int(request.form.get('park'))]
        total_score = round(((sum(ratings)) * 0.4), 1)
        photo = request.files['photo_url']
        photo_upload = cloudinary.uploader.upload(photo, upload_preset="sixbxeod")
        review = {
            'pub_name': request.form.get('pub_name'),
            'pub_address': request.form.get('pub_address'),
            'website': request.form.get('website'),
            'phone_number': request.form.get('phone_number'),
            'review_headline': request.form.get('review_headline'),
            'review_adult': request.form.get('review_adult'),
            'review_kids': request.form.get('review_kids'),
            'service': request.form.get('service'),
            'atmosphere': request.form.get('atmosphere'),
            'food': request.form.get('food'),
            'value': request.form.get('value'),
            'park': request.form.get('park'),
            'total_score': total_score,
            'review_date': request.form.get('review_date'),
            'category_list': request.form.getlist('category_list'),
            'created_by': session['user'],
            'photo_url': photo_upload['secure_url']
        }
        mongo.db.reviews.insert_one(review)
        flash('Review Successfully Added')
        return redirect(url_for('index'))

    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('add_review.html', categories=categories)


@app.route('/edit_review/<review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    """
    This allows a user to edit any aspect of the review. The if statement is there
    to allow users to upload a different photograph.
    """
    if request.method == 'POST':
        ratings = [int(request.form.get('service')),
                   int(request.form.get('atmosphere')),
                   int(request.form.get('food')),
                   int(request.form.get('value')),
                   int(request.form.get('park'))]
        total_score = round(((sum(ratings)) * 0.4), 1)
        if request.form.get('file_name') != mongo.db.reviews.find_one(
                {'_id': ObjectId(review_id)})['photo_url']:
            photo = request.files['photo_url']
            photo_upload = cloudinary.uploader.upload(photo, upload_preset="sixbxeod")
            submit = {
                'pub_name': request.form.get('pub_name'),
                'pub_address': request.form.get('pub_address'),
                'website': request.form.get('website'),
                'phone_number': request.form.get('phone_number'),
                'review_headline': request.form.get('review_headline'),
                'review_adult': request.form.get('review_adult'),
                'review_kids': request.form.get('review_kids'),
                'service': request.form.get('service'),
                'atmosphere': request.form.get('atmosphere'),
                'food': request.form.get('food'),
                'value': request.form.get('value'),
                'park': request.form.get('park'),
                'total_score': total_score,
                'review_date': request.form.get('review_date'),
                'category_list': request.form.getlist('category_list'),
                'created_by': session['user'],
                'photo_url': photo_upload['secure_url']
            }
            mongo.db.reviews.update({'_id': ObjectId(review_id)}, submit)
            flash('Review Successfully Updated')
            return redirect(url_for('read_review', review_id=ObjectId(review_id)))
        photo_url = request.form.get('file_name')
        submit = {
            'pub_name': request.form.get('pub_name'),
            'pub_address': request.form.get('pub_address'),
            'website': request.form.get('website'),
            'phone_number': request.form.get('phone_number'),
            'review_headline': request.form.get('review_headline'),
            'review_adult': request.form.get('review_adult'),
            'review_kids': request.form.get('review_kids'),
            'service': request.form.get('service'),
            'atmosphere': request.form.get('atmosphere'),
            'food': request.form.get('food'),
            'value': request.form.get('value'),
            'park': request.form.get('park'),
            'total_score': total_score,
            'review_date': request.form.get('review_date'),
            'category_list': request.form.getlist('category_list'),
            'created_by': session['user'],
            'photo_url': photo_url
        }
        mongo.db.reviews.update({'_id': ObjectId(review_id)}, submit)
        flash('Review Successfully Updated')
        return redirect(url_for('read_review', review_id=ObjectId(review_id)))


    review = mongo.db.reviews.find_one({'_id': ObjectId(review_id)})
    categories = mongo.db.categories.find().sort('category_name', 1)
    prefilled_categories = []
    for ident in review['category_list']:
        category = mongo.db.categories.find_one({'_id': ObjectId(ident)})
        prefilled_categories.append(category)
    return render_template('edit_review.html',
                           review=review,
                           categories=categories,
                           prefilled_categories=prefilled_categories)


@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    """
    This function deletes a review and then returns you to the main page
    """
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    flash('Review Successfully Deleted')
    return redirect(url_for('index'))


@app.route('/delete_review_profile/<review_id>')
def delete_review_profile(review_id):
    """
    This function deletes a review from the profile page
    and then returns you to your profile
    """
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    flash('Review Successfully Deleted')
    return redirect(url_for('profile', username=session['user']))


@app.route('/get_categories')
def get_categories():
    """
    This function fetches the name of all categories for the user to see them
    """
    categories = list(mongo.db.categories.find().sort('category_name', 1))
    return render_template('categories.html', categories=categories)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """
    This function allows a user to add a new category
    """
    if request.method == 'POST':
        category = {
            'category_name': request.form.get('category_name')
        }
        mongo.db.categories.insert_one(category)
        flash('New Category Added')
        return redirect(url_for('get_categories'))

    return render_template('add_category.html')


@app.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    This function allows the user to change the name of a category
    """
    if request.method == 'POST':
        submit = {
            'category_name': request.form.get('category_name')
        }
        mongo.db.categories.update({'_id': ObjectId(category_id)}, submit)
        flash('Category Successfully Updated')
        return redirect(url_for('get_categories'))

    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    return render_template('edit_category.html', category=category)

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    """
    This function deletes a category and updates all reviews to remove the category
    from its category list array also
    """
    reviews = mongo.db.reviews.find()
    for review in reviews:
        if category_id in review['category_list']:
            edit_array = []
            for category in review['category_list']:
                if category != category_id:
                    edit_array.append(category)
            mongo.db.reviews.update(review, {"$set": {"category_list": edit_array}})
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    flash('Category Successfully Deleted')
    return redirect(url_for('get_categories'))


@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    """
    This function renders the contact form
    """
    return render_template('contact_form.html')

@app.route('/contact_form_success')
def contact_form_success():
    flash('Message successfully sent')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)
