from model import Bird, User, connect_to_db, db
from server import app


def load_birds():
    """Load birds from birds.csv into database."""

    for row in open("birds.csv"):

        species, scientific_name = row.rstrip().split(',')
        bird = Bird(species=species, scientific_name=scientific_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(bird)

    # Once we're done, we should commit our work
    db.session.commit()

def make_users():
    u1 = User(fname='Ashley',lname='Lastname',email='Ashley@cheese.com')
    u1.set_password('hellohello')
    db.session.add(u1)

    u2 = User(fname='Solomon',lname='Bisker',email='Sol@cheese.com')
    u2.set_password('solsol')
    db.session.add(u2)

    u3 = User(fname='Annie',lname='Lyons',email='Annie@cheese.com')
    u3.set_password('borskiborski')
    db.session.add(u3)

    u4 = User(fname='Susanna',lname='Lyons',email='SusAnnie@cheese.com')
    u4.set_password('annieannie')
    db.session.add(u4)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    load_birds()
    make_users()