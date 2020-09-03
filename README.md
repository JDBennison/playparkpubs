# Play Park Pubs
Whilst at the peak of the summer this year I spent an awfully long time trying to find the right pub for my family to go to with nice food and drink for the grown ups and big play park for the kids to keep them occupied. Most websites just focus on the food or drink side of thing and you would have to trawl through comments on trip advisor to see if they had a play park and if it was any good. This website is dedicated to families trying to find somewhere fun for everyone. The website would be based on adult reviews for food and drink and then a review written by the kids for the play parks.
## UX
Here are a list of user stories to describe the kind of people who might use the website
* As a parent I want to find somewhere to have good food and drink
* As a hungry person I want a way to find specific pubs that cater to my tastes so I can find the cuisine I like.
* As a parent I want a pub with a good playground so that my kids will enjoy themselves
* As a pub owner I want a way to contact the reviewers to ask them to review my pub.
* As a reviewer of this website I want a simple interface to upload and edit my reviews

### Links To Wireframes

* [Home](static/wireframes/Home.png)
* [Review](static/wireframes/Review.png)
* [New Review](static/wireframes/NewReview.png)
* [Edit Review](static/wireframes/EditReview.png)
* [Contact Form](static/wireframes/Contact.png)

## Features
Here are a list of the features that I have included in this project and features that are yet to be implemented

### Existing Features
* Recently Reviewed

At the top of the home page it shows the last ten reviews by time they were submitted (not by the date they were visited). This is done using the mongo db sort function
* Search

At the top of the home page there is a search bar which searches using the pub name, address and adult review fields. This is using the indexing function of mongo db.
* Sort By

At the top of the list of reviews the user is given the option of sorting the reviews either alphabetically (ascending and descending), by date reviewed (earliest to latest) and by the overall score of the review.
* Pagination

The list of reviews will show the top ten (depending on how its been sorted) before it breaks up into pagination.
* Category View

As well as being able to add new categories, the author of the posts can add assign the categories when creating a review. Using the category view you can select the category you like and you will see all of the reviews with that category attached.
* Add Review

Simple interface with required elements throughout. Upload photos using Cloudinary which then puts the secure url into the database to call back on it for the reviews. Also has a multiple dropdown for categories. If you add extra categories they will appear on the dropdown.
* Profile

Currently shows all the reviews that a user has written.
* Contact Us

Modal box on every page which brings up from you can use to contact us. Uses EmailJS
* Log In/Register

All of the Add/Edit/Delete functionality is only visible to users who have logged in and registered. Currently very basic functionality on this.

### Features Left to Implement
* Log in/Register
I will be adding in more secure features for the login and making the register hidden so that not everyone can register, only the people invited by us. Also want to hook up emails to verify accounts and the like.
* Profile
Would like more user details and the ability to change password. If users want to see who is reviewing they can click on their names and see who they are and what kind of things they like to make them more human.

Technologies Used
For the basics of front end I mostly used HTML5, CSS3 and Javascript and back end I used Python along with the following libraries and frameworks
* [Materialize](https://materializecss.com/)
	* For formatting and structure
* [JQuery](https://jquery.com/)
	* To initialise materialize components. 
* [Mongo DB](https://www.mongodb.com/)
	* For storing reviews, categories and users in a database.
* [PyMongo](https://pymongo.readthedocs.io/en/stable/)
	* To connect Python up to MongoDB
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
	* For structuring and templating the review
* [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
	* For security features logging in and storing passwords securely.
* [Flask Paginate](https://flask-paginate.readthedocs.io/)
	* To paginate the reviews
* [Font Awesome](https://fontawesome.com/)
	* For icons throughout the website.
* [EmailJS](https://www.emailjs.com/)
	* To connect up the contact form and get it sent to me.
* [Favicon Generator](https://realfavicongenerator.net/)
	* To create the favicon.
* [Cloudinary](https://cloudinary.com)
	* To store photos in the cloud and retrieve URL
