from model import Bird, connect_to_db, db
from server import app


def load_birds():
    """Load birds from birds.csv into database."""

    for row in open("birds.csv"):

        row = row.rstrip()
        bird = Bird(species=row)

        # We need to add to the session or it won't ever be stored
        db.session.add(bird)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    load_birds()
   