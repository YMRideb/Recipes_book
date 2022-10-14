import re  # the regex module
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, EMAIL_REGEX, dB
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_to_validate_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(dB).query_db(query, data)
        
        if len(result) > 0:
            current_user = cls(result[0])
            return current_user
        else:
            return None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(dB).query_db(query, data)
        return result

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", "error_first_name")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", "error_last_name")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_email")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "error_pw")
            is_valid = False
        if not data['pwd_confirm'] == data['password']:
            flash("Passwords must match.", "error_pw_confirm")
            is_valid = False
        return is_valid
    

    # @classmethod
    # def login_user(cls, data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL(dB).query_db(query, data)
    #     if len(result)
        # for row_from_db in result:
        #     user_data = {
        #         "id": row_from_db["id"],
        #         "first_name": row_from_db["first_name"],
        #         "last_name": row_from_db["last_name"],
        #         "email": row_from_db["email"]
        #     }
        #     session['id'] = user_data["id"]
        #     session['first_name'] = user_data["first_name"]
        #     session['last_name'] = user_data["last_name"]
        #     session['email'] = user_data["email"]
        #     return False


    # @classmethod
    # def login_validate(cls, data):
    #     query = "SELECT * FROM users_table WHERE email = %(email)s;"
    #     result = connectToMySQL("users_python").query_db(query, data)
    #     for row_from_db in result:
    #         user_data = {
    #             "id": row_from_db["id"],
    #             "first_name": row_from_db["first_name"],
    #             "last_name": row_from_db["last_name"],
    #             "email": row_from_db["email"],
    #             "password": row_from_db["password"]
    #         }
    #     if (len(result) < 1) or (not bcrypt.check_password_hash(user_data["password"], data["password"])):
    #         return False
    #     return True
