from model import Bird, connect_to_db, db



def load_birds():
    """Load games from data/games.csv into database."""

    for bird in birds(open("/bird.csv")):

        row = row.rstrip()
        bird = Bird(bird_id=bird_id, species=species)

        # We need to add to the session or it won't ever be stored
        db.session.add(bird)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_birds()
   