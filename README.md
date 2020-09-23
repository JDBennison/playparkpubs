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

This would include things like pictures and biography too.
* Condensing reviews

If a user writes more than one review of the same pub I would like to be able to automatically make sure they get put on the same page as opposed to two different pages.
## Technologies Used
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

## Testing


## Deployment
To deploy my application I used Heroku and there were a number of steps to follow before I could do this.
1. To protect all of my environment content variables, I put these in an env.py file and added this to a .gitignore file so they weren't saved on Github for everyone to see. I also added them into Herokus Config Vars for production.
2. I needed to make sure that I had a requirements.txt file with a list of all the packages I had installed to make my application run. In the console I simply typed in ```pip3 freeze > requirements.txt```.
3. Creating a Procfile which is tells Heroku what command to run to make my app work. Mine simply says ```web: python app.py```
4. Connect GitHub to Heroku. I found it much easier to go to the deploy menu on Heroku and connect it directly to my GitHub account so that when I pushed my code, it automatically deployed to Heroku.

NOTE: I must also make sure Flask's debugging is False.

**If there are any problems with deployment there will be a log of the error created which you can view on the Heroku dashboard.**

### Cloning the project
If you wish to clone the project to expand the ideas created there are a number of different ways to do this

#### GitHub
* To manally download it you can go to [my GitHub repo](https://github.com/JDBennison/playparkpubs) and upload it to your IED of choice.
* Install the requirements.txt by typing in ```pip3 install -r requirements.txt```.
* You will also need to update the environment variables before you run the app.
    * app.config['MONGO_DBNAME'] = 'play_park_pubs'
    * app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost')
    * app.secret_key = os.environ.get('SECRET_KEY')

Once done you can run Play Park Pubs by typing ```python3 app.py```

#### CLI
* Type the following into the CLI ```gh repo clone JDBennison/playparkpubs```
* Install the requirements.txt by typing in ```pip3 install -r requirements.txt```.
* You will also need to update the environment variables before you run the app.
    * app.config['MONGO_DBNAME'] = 'play_park_pubs'
    * app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost')
    * app.secret_key = os.environ.get('SECRET_KEY')

Once done you can run Play Park Pubs by typing ```python3 app.py```

## Credits
### Content
All content was written by James Bennison and Victoria Storm with the assistance of Fraser (aged 7) and Evony (aged 5)
### Media
All pictures were taken by James Bennison and Victoria Storm
### Acknowledgments
I'd like to thank my amazing family for going to so many pubs with me to help me review them and for giving me honest feedback on what they thought of said pubs and play parks.

I also need to say that this website has been Victoria's idea for years before I made it a reality.