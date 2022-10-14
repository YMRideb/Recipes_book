from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
bcrypt = Bcrypt(app)

# this route renders if my portal is accessed, if Im not mistaken
@app.route('/')
def index():
    print("show me the money")
    return render_template("index.html")


    # RESTful routing!
    # this route fires a post request to my ctrl files and runs my queries, returning data and redirecting back to the recipes route
    # this route is located @ the top of the index.html
@app.route('/user/register', methods=['POST'])
def register_user():
    if User.validate_user(request.form) == False: #this line calls on the staticmethod validate_user in the user_model file
        return redirect('/')
    user_exists = User.get_one_to_validate_email(request.form) # this line checks if the email already exists
    if user_exists != None:
        flash("Sorry! This email already exists (>_<) ", "error_user_exists")
        return redirect('/')
    data = {
        **request.form,
        'password': bcrypt.generate_password_hash(request.form['password']) # this line is inside of a block that creates a session to carry
    }#                                                                        the users information or "be logged in"
    user_id = User.create(data)
    
    session['first_name'] = data['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id
    return redirect('/recipes')# all of these post requests HAVE to be redirected and all of the information is being passed through
    
    # this route fires a post request to my ctrl files and runs my queries, returning data and redirecting back to the recipes route
    # this route is located @ the middle of the index.html, controlling user logins
@app.route('/user/login', methods=['POST'])
def process_login():
    current_user = User.get_one_to_validate_email(request.form)
    if current_user != None:
        if not bcrypt.check_password_hash(current_user.password, request.form['password']):
            flash("Sorry, your email or password is incorrect. Please enter your information", "error_no_user")
            return redirect('/')
        session['first_name'] = current_user.first_name
        session['email'] = current_user.email
        session['user_id'] = current_user.id
        return redirect('/recipes')
    else:
        flash("Sorry, your email or password is incorrect. Please enter your information", "error_no_user")
        return redirect('/')
# this route just clears the session and effectively logs the user out of this browser
@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')

    # if (User.get_one_email_to_validate(request.form)) == False:
    #     return redirect('/')
    # current_user = User.get_one_email_to_validate(request.form)
    # if current_user == True:
    #     flash("Sorry! This email already exists  ):", "error_user_exists")
    
    # User.create(request.form)
    # return redirect('/') # this will change
    # have to validate if the users password is encrypted
    # then connect to the model
    # data = {
    #     "first_name": request.form["first_name"],
    #     "last_name": request.form["last_name"],
    #     "email": request.form["email"],
    #     "password": pw_hash
    # }
    # passing the User instance data
    
    # User.login_user(data)
    # classmethods for User instances
    # return redirect('/dashboard')
# redirect because its a POST method
                                    # if not User.validate_user(request.form):
                                    #     return redirect('/')
                                    # pw_hash = bcrypt.generate_password_hash(request.form['password'])


        
#     if not is_valid:
#     elif is_valid:
#         User.login_user(request.form)
#         return redirect('/dashboard')


# @app.route('/dashboard')
# def show_dashboard():
#     if 'email' not in session:
#         flash("Sorry, you need an email address to continue.", "error_bad_login")
#         return redirect('/')
#     return render_template('dashboard.html')
