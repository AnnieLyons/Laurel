from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Field_Log, Bird



app = Flask(__name__)

# Required to use Flask sessions and debugging toolbar. 
app.secret_key = b'b\xd4\xa8\xf6#\x13\x14\x95\x8b\xb2\x19\x0c]\xea-\xef\xb0l\xd5\x92\xef\x10_['

# Causes an undefined variable in jinja to throw an error, instead of failing silently. 
app.jinja_env.undefined = StrictUndefined

@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""

    if session.get('user_id'):
        return redirect("/welcome")

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def registration_form():
    """Show form for user signup."""

    return render_template("registration_form.html")


@app.route('/register', methods=['POST'])
def registration_process():
    """Process registration."""

    # Get form variables
    fname = request.form.get("first_name")
    lname = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")


    new_user = User(fname=fname, lname=lname, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {fname} {lname} added.")
    return redirect("/login")    


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")
 

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("So Sorry! Beak Buddy not found.")
        return redirect("/login")

    if not user.check_password(password):
        flash("Password is incorrect.")
        return redirect("/login")

    session["user_id"] = user.user_id
    
    flash(f"Hello, Beak Buddy {user.fname} {user.lname}!")
    return redirect("/welcome")


@app.route('/logout', methods=['GET'])
def logout():
    """Log out."""
    
    session.pop("user_id", None)
    
    flash("Flutter Back Soon!")
    return redirect("/login")


@app.route('/welcome')
def welcome():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    else:
        return render_template("welcome_page.html", user=User.query.get(user_id))
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
