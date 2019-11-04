class User(db.Model): 
    """User information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        )
    fname
    lname
    email
    password
    created_at
    updated_at


class Bird(db.Model): 
    """Bird and species information."""

    __tablename__ = "birds"

    bird_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        )
    species
    created_at
    updated_at


class Field_Log(db.Model): 
    """Log book to track birds seen and related information."""

    __tablename__ = "field_logs"

    log_id = db.Column(db.Integer, 
                       primary_key=True,
                       autoincrement=True,
                       )
    date
    time_of_day
    location
    weather
    habitat
    equipment
    notes
    created_at
    updated_at

    user_id (FK)


class Log_Birds(db.Model):
    """List of all birds seen on a particular day."""

    __tablename__ = "birds_seen"

    log_birds_id = db.Column(db.Integer, 
                             primary_key=True,
                             autoincrement=True,
                             )

    log_id (FK)
    bird_id (FK)


# class TimeStampMixin(object):
    """ Timestamping mixin """  

    # created_at = Column(DateTime, default=datetime.utcnow)
    # created_at._creation_order = 9998  
    # updated_at = Column(DateTime, default=datetime.utcnow)
    # updated_at._creation_order = 9998  

    # @staticmethod  
    # def _updated_at(mapper, connection, target):  
    #     target.updated_at = datetime.utcnow()  

    # @classmethod  
    # def __declare_last__(cls):  
    #     event.listen(cls, 'before_update', cls._updated_at) 

    # https://til.tafkas.net/post/python/auto-timestamping-sqlalchemy-entities/
