# Name: Raluca Ciobanu
# Student Number: c00289426
# Date: November 2024.
# views.py
from app import app, db
from flask import render_template, request, url_for
from app.models import Recipe, RecipeIngredient
from sqlalchemy import func # func.random() used to generate a random recipe

# Displays the home page of the website, which shows a list of recipes.
# The recipes are retrieved from the database using SQLAlchemy's ORM (Object Relational Mapper)  
# The home page also displays a background image, which is retrieved using
# Flask's url_for function.
# The function returns the rendered HTML template for the home page.
@app.route("/", methods=["GET"])
def home():
    # Retrieve all recipes - this line is equivalent to SELECT * FROM RECIPES

    # Fetch a limited number (12) of recipes initially
    per_page = 12
    page = 1
    # The next line is used to implement a form of pagination 
    # Select all recipes and limit to 12 per page
    # Here we multiply the page number by the number of recipes per page and return that set of results
    recipes = Recipe.query.limit(per_page).offset((page - 1) * per_page).all()

    # Get the URL for the home page image
    image_path = url_for('static', filename='images/landing_picture.jpg') 
    # Render a HTML template and return it as a string. 
    # The variables recipes and image_path are passed to the template.
    # These are known as template variables and can be used in the template
    #  to display the data.
    # The value of the page number variable is written back to the rendered HTML page as well.
    return render_template("index.html", recipes=recipes, image_path=image_path, page=page)
  
# This API route is used to search for recipes based on the search text entered by the user
# The search text is passed as a query parameter to the route
# The route returns a list of recipes that match the search text
# If the search text is empty, the route returns an empty list
@app.route('/search', methods=['GET'])
def search():
  
    # Get the search text
    search_text= request.args.get('search-text')
    # If there is no search text, return an empty list
    if not search_text:      
        return render_template("search_results.html", recipes=[])
    # If there is search text, return a list of recipes that match the search text
    else:
        # Get a list of recipe ids that match the search text, joined with the recipe_ingredients table
        # The or condition is used to search for recipes that match the search text in the recipe name or 
        # the recipe ingredients, therefore it is possible that duplicate recipe ids will be returned
        # distinct is used to get a unique list of recipe ids
        recipe_ids = db.session.query(Recipe.recipe_id).join(RecipeIngredient).filter(
        db.or_(
            Recipe.name.like(f'%{search_text}%'),
            RecipeIngredient.ingredient_name.like(f'%{search_text}%')
        )
        ).distinct().all()

        # The recipe_ids list contains tuples of recipe IDs returned by the database query. 
        # Each tuple has only one element, which is the recipe ID.
        # This line of code iterates over each tuple in recipe_ids, extracts the first element 
        # (which is the recipe ID), and adds it to the recipe_ids_list.
        recipe_ids_list = [recipe_id[0] for recipe_id in recipe_ids]
        # Retrieve a list of Recipe objects from the database that match the recipe IDs in the recipe_ids_list.
        # The filter method is used to filter the recipes based on the recipe IDs in the recipe_ids_list
        recipes = Recipe.query.filter(Recipe.recipe_id.in_(recipe_ids_list)).all()               
        return render_template("search_results.html", recipes=recipes)
    

# This API route is used to display the details of a recipe.
# The recipe ID is passed as a query parameter to the route.
# The route returns the details of the recipe.
@app.route('/view/<int:recipe_id>')
def view_recipe(recipe_id):    
    # Retrieve the single recipe from the database
    recipe = Recipe.query.get(recipe_id)
    # Check if the recipe exists    
    if recipe:
        # Retrieve the ingredients for the recipe
        ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()  
        # Render the recipe details template     
        return render_template("recipe_details.html", recipe=recipe, ingredients=recipe.ingredients)
    else:
        return 'Recipe not found', 404


# This API route is used to load more recipes when the user scrolls to the bottom of the page.
# The route returns a list of recipes.
# The number of recipes to load is specified in the per_page variable
@app.route("/load_more/", methods=["GET"])
def load_more():
   
    per_page = 12
    # page 1 is served from the root URL (/) to template index.html
    # The query parameter page-number indicates the *last* page number that
    # was served, so it must be incremented to get the next page.
    page = int(request.args.get('page-number', 1)) + 1      
    recipes = Recipe.query.limit(per_page).offset((page - 1) * per_page).all()
    # if there are no more recipes, ensure page number will not increment
    # indefinitely (page number is written back to the DOM on each response)
    if not recipes:
        page = page - 1  
    return render_template('load_more.html', recipes=recipes, page=page)


# This API route is used to sort the recipes alphabetically.
# The route returns a list of recipes.
@app.route("/view_by_recipe_name", methods=["GET"])
def view_alphabetically():
    per_page = 12
    page = 1
    offset = (page - 1) * per_page
    # The query parameter sort-order indicates the sort order of the recipes
    sort_order = request.args.get("sort_order")
    # If the sort order is "asc" or "desc", sort the recipes alphabetically 
    if sort_order == "asc":
        recipes = Recipe.query.order_by(Recipe.name.asc()).offset(offset).limit(per_page).all()
    elif sort_order == "desc":
        recipes = Recipe.query.order_by(Recipe.name.desc()).offset(offset).limit(per_page).all()
    else: # If the sort order is not "asc" or "desc", then no sorting is applied
        recipes = Recipe.query.limit(per_page).offset((page - 1) * per_page).all()
    return render_template("load_more.html", recipes=recipes, page=page)

# This API route is used to display a random recipe.
# The route returns the details of the recipe.
@app.route("/recipe_of_the_day", methods=["GET"])
def randomRecipe():
    # Retrieve a random recipe, first() is used to retrieve a single record.
    recipe = Recipe.query.order_by(func.random()).first()
    # Render the recipe details template
    return render_template("recipe_of_the_day.html", recipe=recipe)
 
