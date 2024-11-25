# Name: Raluca Ciobanu
# Student Number: c00289426
# Date: November 2024.
# models.py defines the Recipe and RecipeIngredient models 
from app import db

# The class Recipe represents the recipe table in the database
# Recipe is a subclass of db.Model which allows us to interact with the database
class Recipe(db.Model): 
    # The recipe_id is the primary key
    recipe_id = db.Column(db.Integer, primary_key=True)
    # The name of the recipe is stored in the name column and cannot be null
    name = db.Column(db.String(50), nullable=False)
    # The method associated with the recipe and cannot be null
    method = db.Column(db.Text, nullable=False)
    # The image_path of the recipe is stored in the image_path column and cannot be null
    image_path = db.Column(db.String(255), nullable=False)

   
# A Recipe can have many RecipeIngredients
class RecipeIngredient(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
     # The recipe_id is defined as a foreign key in this table 
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))
    # A RecipeIngredient simply has a name
    ingredient_name = db.Column(db.String(50), nullable=False)
    # Establish a relationship between the RecipeIngredient model and the Recipe model
    # The name of this relationship is 'Recipe'
    # backRef crates a bi-directional relationship between the two models.
    # This line allows us to access the Recipe object associated with a RecipeIngredient object
    #  It also permits us to access the list of RecipeIngredient objects associated
    # with a Recipe object using the 'ingredients' attribute.
    # E.g. given a RecipeIngredient ri, we can access the associated Recipe object
    # using ri.recipe
    # Given a Recipe object r, we can access the list of RecipeIngredients using
    # r.ingredients
    # lazy=True means that the relationship will be loaded on first access
    recipe = db.relationship('Recipe', backref=db.backref('ingredients', lazy=True))