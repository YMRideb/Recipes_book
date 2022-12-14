from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import dB
from flask_app.models.user_model import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def create (cls, data):
        query = "INSERT INTO recipes(name, description, instructions, cooked_date, under_30, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL(dB).query_db(query, data)
            # you could also set connectToMySQL to something like results and return that instead
    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        
        results = connectToMySQL(dB).query_db(query)
        list_recipes = []
        for row in results:
            current_recipe = cls(row)
            user_data = {
                **row,
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "id" : row['users.id']
            }
            current_user = User(user_data) 
            current_recipe.user = current_user
            list_recipes.append(current_recipe)
        return list_recipes

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(dB).query_db(query, data)
        if len(result) > 0:
            current_recipe = cls(result[0])
            user_data = {
                **result[0],
                "created_at" : result[0]['users.created_at'],
                "updated_at" : result[0]['users.updated_at'],
                "id" : result[0]['users.id']
            }
            current_recipe.user = User(user_data)
            return current_recipe
        else:
            return None
        
    @classmethod
    def update_one(cls, data):
        query="UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, under_30 = %(under_30)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(dB).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(dB).query_db(query, data)

    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if data['name'] == "":
            flash("Your recipe must have a name (>_<)", "error_recipe_name")
            is_valid = False
        if data['description'] == "":
            flash("Your recipe must have a description (>_<)", "error_recipe_description")
            is_valid = False
        if data['instructions'] == "":
            flash("Your recipe must have some instructions (>_<)", "error_recipe_instructions")
            is_valid = False
        if data['cooked_date'] == "":
            flash("Your recipe must have a cooked_date (>_<)", "error_recipe_cooked_date")
            is_valid = False
        if len(data['name']) < 3:
            flash("Your recipe name must have 3 or more characters (O_O)", "error_recipe_char")
            is_valid = False
        if len(data['description']) < 3:
            flash("Your recipe description must have 3 or more characters (O_O)", "error_recipe_descript")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Your recipe instructions must have 3 or more characters (O_O)", "error_recipe_instruct")
            is_valid = False
        return is_valid
            