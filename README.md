# Recipes_book
## Python + Flask + MySQL
### This is a small, scalable web app that allows a user to create a profile and add their personal favorite recipes!


- Using Flask-Bcrypt, users login and registration information is hashed and secure
  - Users can view other recipes, but can only **edit** or **delete** their own recipes
- With the Jinja2 python library, client and server files are able to communicate with MySQL db
- Utilizing the Bootstrap library, the client-facing end is easily navigable
  The flask_app directory is divided into four sub-directories, with an init.py file to run the app
  
  1. config
      - Contains the scripting to connect Python server files with MySQL database, and error messaging for server
    
  2. controllers
      - Contains routes to render the browser HTML and CSS elements displayed on the client-side
      - Two files, one for the user routes and one for recipes routes
    
  3.  models
      - Contains python classmethods and staticmethods which serve as instances of MySQL database
      - Two files, one for the user model instances, and one for the recipes model instances
    
  4. templates
      - Contains html files that are displayed on the client-side, built with Jinja2 and Bootstrap

The login and registration functionality utilizes session, or "cookies" to store the current user's data and validates which user is currently viewing the app. The back-end validations in the model files, or ```staticmethod``` functions serve to make sure that data submitted by the user to the database is formatted correctly.
