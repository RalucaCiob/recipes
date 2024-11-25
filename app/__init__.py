# Name: Raluca Ciobanu
# Student Number: c00289426
# Date: November 2024.
# __init__.py sets up the Flask application and initialises the database.
# sqlite3 database is used for testing on localhost, but PostgreSQL is used for production.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import csv

# If the environment variable PERSISTENT_STORAGE_DIR is set, it's value is used
# as the persistent_path, otherwise the absolute path of the current Python file
# is used.
# This line provides a way to configure the directory where the sqlite database is stored.
# This is useful for testing the web app on localhost without requiring a separate database server.
persistent_path = os.getenv("PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__)))

# Creates an instance of the Flask web framework using the name of the current module
app = Flask(__name__)


EXPLAIN_TEMPLATE_LOADING=True
app.logger.setLevel("INFO")

# Set the path to the sqlite database file
db_path = os.path.join(persistent_path, "sqlite.db")

# Define some configuration settings for the Flask-SQLAlchemy extension
# Set the URI of the key SQLALCHEMY_DATABASE_URI to a string 
# like sqlite:///path/to/db/sqlite.db
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'

# This config is for the PostgreSQL database.
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mysecretpassword@localhost:5432/mydatabase"

# Stop SQLAlchemy printing SQL statements as they are executed.
app.config["SQLALCHEMY_ECHO"] = False
# Don't track changes to the database (e.g. schema or data) 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Make an instance of SQLAlchemy
db = SQLAlchemy()

# This function is used to create the database tables and is called once only.
def create_database():
     db.create_all()
# This function is used to initially populate the database with some 
# sample records. The data is loaded from a text file called "test_data.txt"
# The data is comma separated (CSV) where each line is of the format:
# recipe_name, path_to_recipe_image, ingredient_name_1, ingredient_name_2 etc
# The number of ingredients can vary per recipe.

def load_test_data():
    from app.models import Recipe, RecipeIngredient  
    # Only populate the database with some sample records if it is empty
    if Recipe.query.count() == 0:
        with open('test_data.txt', 'r') as file:
            reader = csv.reader(file)
            # loop through each line (row) in the text file, split each row
            # into a list of values that can be accessed by an index.        
            for row in reader:
                # e.g. index 0 is the recipe name   
                recipe_name = row[0]
                image_path = row[1]
                method = row[2]
                # There are a variable number of ingredients
                # They are split into a list of strings using "," as a delimiter
                # ingredient_names = row[3].split(',')
                ingredient_names = row[3:]               
                recipe = Recipe(name=recipe_name, method=method, image_path=image_path)
                db.session.add(recipe)
                for ingredient_name in ingredient_names:
                    ingredient_name = ingredient_name.strip()
                    recipe.ingredients.append(RecipeIngredient(ingredient_name=ingredient_name))
                db.session.add(recipe)              
        db.session.commit()

# This function is called after the db.init_app is called below.
def init_db():
    create_database()
    load_test_data()

from app import views
from app import models

# Initialises the Flask-SQLAlchemy database instance (db) with the Flask application instance (app).
# Binds the database instance to the application, allowing the application to use the database connection. 
# This is a necessary step to use the database with the Flask application.
db.init_app(app)

# Call the init_db function to create the database tables and load the test data
with app.app_context():
    init_db()
