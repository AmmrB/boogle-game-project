from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('score'))
            self.assertIn(b'<table>', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in session"""

        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["U", "H", "D", "K"],
                                           ["U", "N", "E", "O"],
                                           ["W", "R", "K", "V"],
                                           ["I", "O", "A", "G"],
                                           ]
            response = self.client.post('/check-word', json={"word": "WORD"})
            self.assertEqual(response.json['result'], 'ok')
            self.assertEqual(response.json['score'], 4)

    def test_reset_game(self):
        """Test if game can be reset"""

        with self.client as client:
            response = self.client.post('/reset')
            self.assertIn('board', session)
            self.assertEqual(session['score'], 0)
            self.assertEqual(session['played'], 1)
            self.assertEqual(session['highest_score'], 0)

if __name__ == '__main__':
    unittest.main()
