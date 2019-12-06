import unittest
from server import app
from model import connect_to_db, db, User, Field_Log, Bird, bird_field_log_association_table
from seed import make_users

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask Routes."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = app.test_client()
        connect_to_db(app, db_uri='postgresql:///testdb')
        db.create_all()
        #example_data will error out atm, need to create
        make_users()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_welcome(self):
        """Test welcome page initial rendering"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Welcome", result.data)

    def test_register(self):
        """Test registration page intital rendering"""
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Register", result.data)

    def test_login_form(self):
        """Test login page intial rendering"""
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Welcome", result.data)


    def test_logout_form(self):
        """Test logout page intial rendering"""
        result = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Flutter Back Soon!", result.data)
        
    def test_bird_search(self):
        """Test logout page intial rendering"""
        result = self.client.get('/bird_search')
        self.assertEqual(result.status_code, 200)
        # self.assertIn(b"search_term", result.data)    

        # Is redirecting to Login because of the session user_id... 
        # without follow_redirects=True it gets a 302 status code.
    # def test_homepage(self):
    #     """Test homepage initial rendering"""
    #     result = self.client.get('/homepage', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Hello", result.data)   

    # def test_new_log_entry(self):
    #     """Test make new log page initial rendering"""
    #     result = self.client.get('/new_log_entry', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Let birding commence!", result.data)  

    # def test_recent_ebirds(self):
    #     """Test logout page intial rendering"""
    #     result = self.client.get('/recent_ebirds', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Cornell Lab of Ornithology", result.data)

    # def test_view_past_logs(self):
    #     """Test view past logs page intial rendering"""
    #     result = self.client.get('/view_past_logs', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Which past log", result.data)

    # def test_view_past_log(self):
    #     """Test view_past_log page intial rendering"""
    #     result = self.client.get('/view_past_log/<log_id>', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"peek into the past", result.data)

    # def test_stats(self):
    #     """Test stats page intial rendering"""
    #     result = self.client.get('/stats', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Your bird stats", result.data)

    # def test_all_birds_seen(self):
    #     """Test all_birds_seen page intial rendering"""
    #     result = self.client.get('/all_birds_seen', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"identified species", result.data)

    # def test_most_seen_birds(self):
    #     """Test most_seen_birds page intial rendering"""
    #     result = self.client.get('/most_seen_birds', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"frequently seen birds", result.data)

    # def test_bird_map(self):
    #     """Test bird map page intial rendering"""
    #     result = self.client.get('/bird_map', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Map your logs", result.data)

    # def test_resources(self):
    #     """Test resources page intial rendering"""
    #     result = self.client.get('/resources', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Helpful resources", result.data)

    # def test_account(self):
    #     """Test account page intial rendering"""
    #     result = self.client.get('/account', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Account Information", result.data)

    # def test_update_name(self):
    #     """Test update name page intial rendering"""
    #     result = self.client.get('/update_name', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"update your name", result.data)

    # def test_change_password(self):
    #     """Test change_password page intial rendering"""
    #     result = self.client.get('/change_password', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Verify New Password", result.data)

    # def test_update_email(self):
    #     """Test update email page intial rendering"""
    #     result = self.client.get('/update_email', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"New email address", result.data)

    # def test_contact(self):
    #     """Test contact page intial rendering"""
    #     result = self.client.get('/contact', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Contact", result.data)

    # def test_credits(self):
    #      """Test credits page intial rendering"""
    #      result = self.client.get('/credits', follow_redirects=True)
    #      self.assertEqual(result.status_code, 200)
    #      self.assertIn(b"In Loving Memory", result.data)


if __name__ == '__main__':
    unittest.main()