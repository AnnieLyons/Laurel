from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Field_Log, Bird



app = Flask(__name__)

# Required to use Flask sessions and debugging toolbar. 
app.secret_key = b'b\xd4\xa8\xf6#\x13\x14\x95\x8b\xb2\x19\x0c]\xea-\xef\xb0l\xd5\x92\xef\x10_['

# Causes an undefined variable in jinja to throw an error, instead of failing silently. 
app.jinja_env.undefined = StrictUndefined

@app.route("/", methods=['GET'])
def welcome():
    """Show the welcome page."""

    if get_current_user_id():
        return redirect("/homepage")

    return render_template("welcome_page.html")


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
    return redirect("/homepage")


@app.route('/logout', methods=['GET'])
def logout():
    """Log out."""
    
    #Remove user from session
    session.pop("user_id", None)
    
    flash("Flutter Back Soon!")
    return redirect("/login")


@app.route('/homepage', methods=['GET'])
def homepage():
    """Display site homepage."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("homepage.html", user=User.query.get(user_id))



@app.route('/new_log_entry', methods=['GET'])
def new_log_form():
    """Show new log form."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("new_log_form.html", user=User.query.get(user_id), birds=Bird.query.all())

@app.route('/new_log_entry', methods=['POST'])
def new_log_process():
    """Process new log."""

    # Get form variables
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    weather = request.form.get("weather")
    habitat = request.form.get("habitat")
    equipment = request.form.get("equipment")
    notes = request.form.get("notes")

    # Convert list of string bird_id's into integers.
    bird_ids = [int(i) for i in request.form.getlist("bird_select")]

    new_log = Field_Log(date=date, time=time, location=location, 
                        weather=weather, habitat=habitat, equipment=equipment, 
                        notes=notes)

    # Get the bird_id out of the list.
    for bird_id in bird_ids:
        #Use bird_id to make bird object and append to new_log.
        new_log.birds.append(Bird.query.get(bird_id))

    new_log.user = User.query.get(get_current_user_id())

    db.session.add(new_log)
    db.session.commit()
    
    flash("Your new log has been added!")
    return redirect("/homepage")


@app.route('/bird_search', methods=['GET'])
def bird_search(): 
    """Search db for bird, and return matches."""

    search_term = request.args.get("search_term")

    birds = Bird.query.filter(Bird.species.ilike(f'%{search_term}%')).all()
    bird_results = {"results": [{"id": bird.bird_id, "text": bird.species} for bird in birds]}

    return jsonify(bird_results)


@app.route('/view_past_logs', methods=['GET'])
def past_logs():
    """Show past log selector page."""

    current_user_id = get_current_user_id()
    current_user = get_current_user()
    user_logs = current_user.field_logs

    if not current_user_id:
        return redirect("/login")
    
    return render_template("all_past_logs.html", user_logs=user_logs)


@app.route('/view_past_log/<log_id>', methods=['GET'])
def past_log(log_id):
    """Show past log page."""

    current_user_id = get_current_user_id()

    if not current_user_id:
        return redirect("/login")
    
    return render_template("past_log.html", log=Field_Log.query.get(log_id))


@app.route('/stats', methods=['GET'])
def stats():
    """Show user bird stat options."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("stats.html", user=User.query.get(user_id))


@app.route('/all_birds_seen', methods=['GET'])
def all_birds_seen():
    """Show user all logged birds"""

    current_user_id = get_current_user_id()
    current_user = get_current_user()
    user_logs = current_user.field_logs.species

    if not current_user_id:
        return redirect("/login")
    else:
        return render_template("all_birds_seen.html", speciess="species")        



# @app.route('/most_seen_birds', methods=['GET'])
# def most_seen_birds(): 
#     """Show user most commonly logged birds."""

#     user_id = get_current_user_id()

#     if not user_id:
#         return redirect("/login")
#     else:
#         return render_template("most_seen_birds.html", user=User.query.get(user_id))


@app.route('/resources', methods=['GET'])
def resources(): 
    """Show avalible resources."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("resources.html", user=User.query.get(user_id))


@app.route('/account', methods=['GET'])
def account():
    """Show account information such as email and password."""
    
    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
  
    return render_template("account.html", user=User.query.get(user_id))
   

@app.route('/update_name', methods=['GET'])
def update_name_form():
    """Show update name form."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("update_name_form.html")
    

@app.route('/update_name', methods=['POST'])
def process_update_name():
    """Update user name."""
   
    current_user = get_current_user()
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    
    current_user.fname = fname
    current_user.lname = lname

    db.session.commit()

    flash("Your name has been changed. Please log in again. :)")
    return redirect("/logout")


@app.route('/update_email', methods=['GET'])
def update_email_form():
    """Show update email form."""
    
    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("update_email_form.html")

@app.route('/update_email', methods=['POST'])
def process_update_email():
    """Update user email."""
    
    current_user = get_current_user()
    email = request.form.get("email")
    
    current_user.email = email

    db.session.commit()

    flash("Your email has been changed. Please log in again. :)")
    return redirect("/logout")


@app.route('/change_password', methods=['GET'])
def change_password_form():
    """Show change password form."""
    
    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("change_password_form.html")


@app.route('/change_password', methods=['POST'])
def process_change_password():
    """Change users password."""
    
    user = get_current_user()
    password = request.form.get("password")
    new_password = request.form.get("new_password")
    new_password_check = request.form.get("new_password_check")

    # Check if current password matches password stored in db.
    if not user.check_password(password): 
        flash("Password is incorrect.") 
    # Check if new passwords match.    
    elif new_password != new_password_check:
        flash("Passwords do not match.")
    # Both passwords match, set new password in db.    
    else:
        user.set_password(new_password)
        db.session.commit()
        flash("Password has been changed. Please log in again. :)")
        return redirect("/logout")

    return redirect("/change_password")


@app.route('/contact', methods=['GET'])
def contact():
    """Display contact information."""

    user_id = get_current_user_id()

    if not user_id:
        return redirect("/login")
    
    return render_template("contact.html")


def get_current_user():
    """Returns user object for current user_id."""

    return User.query.get(get_current_user_id())


def get_current_user_id():
    """Returns current user id."""

    return session.get("user_id")

# def check_user_in_session(): 
#     """Checks if user_id is in session. If not, redirects to log in."""
    
#     user_id = get_current_user_id()

#     if not user_id:
#         return redirect("/login")

#  Come back to this .....

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
