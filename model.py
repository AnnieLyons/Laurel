
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model): 
    """User information."""
    
    # This Table has a backref relationship with the Field_log Table.

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        nullable=False
                        )
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Show helpful user information."""
        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}"


# Association Table with the log_id's and bird_id's.
bird_field_log_association_table = db.Table('birds_field_logs',
    db.Column('log_id', db.Integer, db.ForeignKey('field_logs.log_id')),
    db.Column('bird_id', db.Integer, db.ForeignKey('birds.bird_id'))
)


class Bird(db.Model): 
    """Bird and species information."""

    __tablename__ = "birds"

    bird_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        nullable=False
                        )
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    species = db.Column(db.String(75), nullable=False, unique=True)
    scientific_name = db.Column(db.String(150), nullable=False, unique=True)

    field_logs = db.relationship('Field_Log', 
                                 secondary=bird_field_log_association_table, 
                                 backref='birds') 

    def __repr__(self):
        """Show helpful bird information."""
        return f"<Bird bird_id={self.bird_id} species={self.species}"



class Field_Log(db.Model): 
    """Log book to track birds seen and related information."""

    __tablename__ = "field_logs"

    log_id = db.Column(db.Integer, 
                       primary_key=True,
                       autoincrement=True,
                       nullable=False
                       )
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # When creating data for date and time, remember to use datetime.date/time.
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location_nickname = db.Column(db.String(100))
    location = db.Column(db.String(100), nullable=False)
    
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float) 
    
    weather = db.Column(db.String(100))
    habitat = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    user = db.relationship('User', backref=db.backref('field_logs', order_by='Field_Log.date'))
    
    def __repr__(self):
        """Show helpful field log information."""
        return f"<Field_Log log_id={self.log_id} date={self.date} location={self.location}"


def connect_to_db(app, db_uri="postgres:///laurel"):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)


