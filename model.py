
from datetime import datetime
import enum
import flask 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(UserMixin, db.Model): 
    """User information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        )
    fname = db.Column(db.String(50), nullable=False,)
    lname = db.Column(db.String(50), nullable=False,)
    email = db.Column(db.String(100), nullable=False, unique=True,)
    '''
    password_hash = db.Column(db.String(50), nullable=False,)
    '''
    created_at = db.Column(db.DateTime, db.default=datetime.now)
    updated_at = db.Column(db.DateTime, db.onupdate=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    db.session.add()
    db.session.commit()

    def __repr__(self):
    """Show user information."""
        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lanme} email={self.email}"

class Bird(db.Model): 
    """Bird and species information."""

    __tablename__ = "birds"

    bird_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        )
    '''
    species = db.Column(db.String(75), nullable=False, unique=True,)..... Use Enum?
    '''
    created_at = db.Column(db.DateTime, db.default=datetime.now)
    updated_at = db.Column(db.DateTime, db.onupdate=datetime.now)

    db.session.add()
    db.session.commit()

class Field_Log(db.Model): 
    """Log book to track birds seen and related information."""

    __tablename__ = "field_logs"

    log_id = db.Column(db.Integer, 
                       primary_key=True,
                       autoincrement=True,
                       )
    '''
    date = db.Column(db.Date)......
    time = db.Column(db.Time)......
    '''
    location = db.Column(db.String(100), nullable=False,)
    weather = db.Column(db.String(100),)
    habitat = db.Column(db.String(100),)
    equipment = db.Column(db.String(100),)
    notes = db.Column(db.Text,)
    created_at = db.Column(db.DateTime, db.default=datetime.now)
    updated_at = db.Column(db.DateTime, db.onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    db.session.add()
    db.session.commit()


    def __repr__(self):
    """Show field log information."""
        return f"<Feild_Log log_id={self.log_id} date={self.date} location={self.location}"

class Log_Birds(db.Model):
    """List of all birds seen on a particular day."""

    __tablename__ = "birds_seen"

    log_birds_id = db.Column(db.Integer, 
                             primary_key=True,
                             autoincrement=True,
                             )

    log_id = db.Column(db.Integer, db.ForeignKey('field_logs.log_id'))
    bird_id = db.Column(db.Integer, db.ForeignKey('birds.brid_id'))

    db.session.add()
    db.session.commit()

    def __repr__(self):
    """Show birds in curent log."""
        return f"<Birds birds_seen={self.log_birds_id} current_log={self.log_id}"


"""
***RESOURCE LIST***

- https://docs.sqlalchemy.org/en/13/core/defaults.html
- https://docs.sqlalchemy.org/en/13/core/type_basics.html
- https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem

"""
