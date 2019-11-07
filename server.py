from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and debugging toolbar. 
app.secret_key = "ABC"

# Causes an undefined variable in jinja to throw an error, instead of failing silently. 
app.jinja_env.undefined = StrictUndefined

@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def registration_form():
    """Show form for user signup."""

    return render_template("registration _form.html")


@app.route('/register', methods=['POST'])
def registration_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password_hash = request.form["password"]


    new_user = User(fname=fname, lname=lname, email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {fname}, {lname} added.")
    return redirect(f"/users/{new_user.user_id}")    


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")
 

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password_hash = request.form["password_hash"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("So Sorry! User not found.")
        return redirect("/login")

    if user.password_hash != password_hash:
        flash("Password is incorrect")
        return redirect("/login")

    '''
    # Do I need to be working in a session?....
    session["user_id"] = user.user_id
    '''
    flash("Hello, bird of a feather!")
    return redirect(f"/welecome/{user.user_id}")


@app.route('/logout', methods=['GET'])
def logout():
    """Log out."""
    '''
    # Do I need to be working in a session and del the session info?....
    del session["user_id"]
    '''
    
    return render_template("logout.html")


# @app.route('/Welcome')
# def welcome():

#     event listeners will route to: 
#     create new log
#     view past logs
#     stats page
#     resources page
     
#     navbar has hamburger with logout, account, contact

#     pass


# @app.route('/New_Log_Entry')
# def ():
#     pass
#     #event listeners will route to: 
#     # view past logs
#     # stats page
#     # resources page
#     # 
#     # navbar has hamburger with logout, account, contact
#     # 
#     # navbar has hamburger with logout, account, contact

# @app.route('/View_Past_Logs')
# def
#     pass
#     #event listeners will route to: 
#     # create new log
#     # stats page
#     # resources page
#     # 
#     # navbar has hamburger with logout, account, contact
#     # 
#     # navbar has hamburger with logout, account, contact

# @app.route('/View_Stats')
# def
#     pass
#     #event listeners will route to: 
#     # create new log
#     # view past logs
#     # resources page
#     # 
#     # navbar has hamburger with logout, account, contact
#     # 
#     # navbar has hamburger with logout, account, contact

# @app.route('/Resources')
# def
#     pass
#     #event listeners will route to: 
#     # create new log
#     # view past logs
#     # stats page
#     # 
#     # navbar has hamburger with logout, account, contact
#     # 
#     # navbar has hamburger with logout, account, contact


# @app.route('/Account_Settings')
# def ():
#     pass
#     #Route to /Welcome


# @app.route('/Contact_Us')
# def ():
#     pass
#     #Route to /Welcome




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
