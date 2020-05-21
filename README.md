Musical Venue and Artist Booking Site
-----

*This is a completed project from the Udacity Nanodegree program to demonstrate capability with Python/Flask, not an original idea/creation*

### Introduction

This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Built out the data models to power the API endpoints by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues so a user can:

* create new venues, artists, and shows
* search for venues and artists
* learn more about a specific artist or venue

### Tech Stack

* **SQLAlchemy ORM** - ORM library
* **PostgreSQL** - database 
* **Python3** - server language
* **Flask** - server framework
* **Flask-Migrate** - creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for frontend

### Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
                    "python3 app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py 
  ├── models.py
  ├── requirements.txt *** dependencies "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

* Models in `models.py`
* Controllers in `app.py`
* The web frontend is located in `templates/`
* Web forms for creating data in `form.py`

### Process

  1. Connected to local database in `config.py`
  2. Using SQLAlchemy, set up models for those in `/models.py`. Implemented missing model properties and relationships using database migrations via Flask-Migrate.
  3. Implemented form submissions for creating new Venues, Artists, and Shows with proper constraints, powering the `/create` endpoints, to avoid duplicate or nonsensical form submissions
  4. Implemented the controllers for listing venues, artists, and shows
  5. Implemented search, powering the `/search` endpoints
  6. Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages

### Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)