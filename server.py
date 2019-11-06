from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db



app = Flask(__name__)

app.secret_key = "ABC"

@app.route("/")
def homepage():
    """Show the homepage."""

    return "This is the homepage."


# @app.route('/Register')
# def
#     pass
#     #route to /signin


# @app.route('/Sign_In')
# def
#     pass 
#     #route to /welcome 
 

# @app.route('/Welcome')
# def

#     #event listeners will route to: 
#     # create new log
#     # view past logs
#     # stats page
#     # resources page
#     # 
#     # navbar has hamburger with logout, account, contact

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

# @app.route('/Log_Out')
# def ():
#     pass
#     #Route to /Homepage

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
