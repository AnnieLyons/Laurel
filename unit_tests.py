import unittest
from server import app
from model import connect_to_db, db, User, Field_Log, Bird, bird_field_log_association_table
import sqlite3

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask Routes."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app = app.test_client()
        db.app = app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_unique_email(self):
        """Ensure user email addresses are unique."""

        u1 = User(fname="Jane", lname="Doe", email="jdoe@gmail.com")
        u1.set_password('test1')
        db.session.add(u1)
        db.session.commit()

        u2 = User(fname="John", lname="Doe", email="jdoe@gmail.com")
        u2.set_password("this should fail")
        db.session.add(u2)

        with self.assertRaises(sqlite3.IntegrityError) as context:
            db.session.commit()

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))

    def test_check_password(self):
        pass

    def test_change_name(self):
        pass


if __name__ == '__main__':
    unittest.main()