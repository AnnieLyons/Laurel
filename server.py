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
def welcome():
    """Show the welcome page."""

    if session.get('user_id'):
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

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    else:
        return render_template("homepage.html", user=User.query.get(user_id))



@app.route('/new_log_entry', methods=['GET'])
def new_log_form():
    """Show new log form."""

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    else:
        return render_template("new_log_form.html", user=User.query.get(user_id))

@app.route('/new_log_entry', methods=['POST'])
def new_log_process():
    """Process new log."""
        
    user_id = session.get("user_id")

    # Get form variables
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    weather = request.form.get("weather")
    habitat = request.form.get("habitat")
    equipment = request.form.get("equipment")
    notes = request.form.get("notes")

    new_log = Field_Log(date=date, time=time, location=location, 
                        weather=weather, habitat=habitat, equipment=equipment, 
                        notes=notes)

    user=User.query.get(user_id)
    user.field_logs.append(new_log)

    db.session.add(new_log)
    db.session.commit()
    
    flash("Your new log has been added!")
    return redirect("/homepage")


@app.route('/view_past_logs', methods=['GET'])
def past_logs():
    """Show past log selector page."""

    current_user_id = session.get("user_id")
    current_user = User.query.get(current_user_id)
    user_logs = current_user.field_logs

    if not current_user_id:
        return redirect("/login")
    else:
        return render_template("all_past_logs.html", user_logs=user_logs)


@app.route('/view_past_log/<log_id>', methods=['GET'])
def past_log(log_id):
    """Show past log page."""

    current_user_id = session.get("user_id")


    if not current_user_id:
        return redirect("/login")
    else:
        return render_template("past_log.html", log=Field_Log.query.get(log_id))






@app.route('/stats', methods=['GET'])
def stats():
    """Show user bird stats."""

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    else:
        return render_template("stats.html", user=User.query.get(user_id))


@app.route('/resources', methods=['GET'])
def resources(): 
    """Show avalible resources."""

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    else:
        return render_template("resources.html", user=User.query.get(user_id))


# @app.route('/Account_Settings')
# def account():
# """Manage account settings such as email and password."""
#     pass
#     #Route to /homepage


# @app.route('/Contact_Us')
# def contact():
# """Display contact information."""
#     pass
#     #Route to /homepage




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
