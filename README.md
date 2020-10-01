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
* Search by closest to

I would like users to be able to type their postcode in and be able to see a list of results based on how close the pubs are to them. I would also like to add in a google maps API to show all of the pubs on a map for users to search visually too.
* Image carousel

I am planning to implement a way to let users upload more than one image so that at the bottom of the page there will be a carousel of all the images so that users can see a selection of pictures.
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
The appropriate validators have been used with no warnings for HTML, CSS, Javascript and Python. Manual testing was used extensively with there being no dead links.
In regards to the original UX customer stories, the testing went as follows.
* *As a parent I want to find somewhere to have good food and drink.* - I have provided a number of ways for customers to do this. On the main page it shows a list of reviews with the most recent reviews shown at the top of the page. This is done based on the inbuilt date element of the ID in MongoDB as opposed to the "date reviewed" field. So if a review put the review date for last month then their review would still appear at the top of the list because it was submitted today.

    There is a search bar at the top which looks through the name of the pub, the address of the pub (so you can just type in the town where you are), and also the main bulk of the review for any keywords. If there are no results a warning appears and you can reset the results to get it back to the main homepage. These are paginated if there are more than 10 results.

    There is also a "sort by" drop down so you can view the reviews in different ways. By the date reviewed (by default, most recent first but you can look at the oldest), alphabetically (ascending and descending) and by the reviews with the highest rating also. These are all paginated also.
* *As a hungry person I want a way to find specific pubs that cater to my tastes so I can find the cuisine I like.* - There are various categories of food that reviewers can apply to each of the reviews. The reviewers also have a page where they can add extra categories in if there is something that hasn't been seen before. Reviewers that are logged in can also delete the categories with a confirmation message appearing to confirm they want to delete. This then removes the category from every review also.

    As a user you can then click on the categories section and see all the categories, clicking on the one which you are interested in will then take you to all the reviews that have that category. These are paginated if there are over ten.

    If you are looking at a review and see a category you are interested in you can click on that category and it will take you to a page which shows all the other reviews with that same cuisine.
* *As a parent I want a pub with a good playground so that my kids will enjoy themselves.* - As well as the reviews from kids about the playgrounds and the ratings for the park specifically, we have tried, where possible, to make sure that all of the main images of the reviews are of the play parks so it is the first thing you see for each pub.

    With the pictures you can upload any image file and it gets uploaded to Cloudinary, cropped and resized to be a square image. This works for all image types and will convert them all to jpgs.
* *As a pub owner I want a way to contact the reviewers to ask them to review my pub.* - In the footer of each page there is a link for a contact form. Originally this was going to be modal but I found that no matter whether the form was submitted or not, clicking submit would close the modal so I converted this to a separate page which also has helped to put in a flash message which lets users know they have been successful.

    During testing, this form does not submit unless every field has been filled in using the Materialize in built validation tools.
* *As a reviewer of this website I want a simple interface to upload and edit my reviews.* - The add review button is always in the header when you are a logged in user, not if you are a regular user. The add review page and edit review page are the same except for the edit page being prefilled with the current values.

    The add review page will not submit unless all fields are filled in, again using materialize's validation tools. For ease I have added a datepicker for the Date Visited field, a multiple selector for the category list (which dynamically updates when new categories are added) and sliders for the different ratings at the bottom. The sliders automatically calculate the total score based on the five different ratings given.

    One particular bug which I have been unable to solve currently is in the category selector. This is the only thing that doesn't work with the valdiator. With any other field, if not filled in, there will be a pop up box to inform the user that they need to do so. With the selector, no such box appears, it does not change to red and the form is not submitted. This means that the user might not realise what is wrong with it and wont know why the form isnt submitting. I'm yet to work out how to fix this.

In relation to the screen size alterations, mostly they remain the same, except for how many reviews show within a row. The main difference is on the index page, where the most recent box gets removed on smaller screens as it doesn't flow as nicely for the user.

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