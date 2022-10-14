from flask_app import app
from flask import render_template,request,redirect,flash
from flask_app.controllers import user_ctrl, recipes_ctrl



if __name__=="__main__":
    app.run(debug=True) 