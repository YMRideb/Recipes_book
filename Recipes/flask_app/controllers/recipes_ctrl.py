from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe_model import Recipe

# move this controller to recipes_ctrl
@app.route('/recipes')
def display_recipes():
    if 'email' not in session:
        flash("This page is only available to users logged in. Please login to continue", "error_force_login")
        return redirect('/')
    list_recipes = Recipe.get_all_with_users()
    return render_template('dashboard.html', list_recipes = list_recipes)


@app.route('/recipe/new')
def display_recipe_create():
    if 'email' not in session:
        flash("This page is only available to users logged in. Please login to continue", "error_force_login")
        return redirect('/')
    return render_template("create_recipe.html")


@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if Recipe.validate_recipe(request.form) == False:
        return redirect('/recipe/new')
    # Create the recipe
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    Recipe.create(data)
    # redirect to the /recipes
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def display_one_recipe(id):
    if 'email' not in session:
        flash("This page is only available to users logged in. Please login to continue", "error_force_login")
        return redirect('/')
    data ={
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user(data)
    return render_template("recipe.html", current_recipe=current_recipe)


@app.route('/recipes/<int:id>/edit')
def display_update_recipe(id):
    if 'email' not in session:
        flash("This page is only available to users logged in. Please login to continue", "error_force_login")
        return redirect('/')
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user(data)
    return render_template("update_recipe.html", current_recipe = current_recipe)


@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_one_recipe(id):
        if Recipe.validate_recipe(request.form) == False:
            return redirect(f'/recipes/{id}/edit')
        recipe_data = {
            **request.form,
            "id": id,
            "user_id" : session['user_id']
        }
        Recipe.update_one(recipe_data)
        return redirect('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    flowers = {
        "id" : id
    }
    Recipe.delete_recipe(flowers)
    return redirect('/recipes')
    # if Recipe.validate_recipe(request.form) == False:
    #     return redirect(f'/recipes/{id}/edit')
