# project/test.py

import unittest

from project import app

class ProjectTests(unittest.TestCase):
    '''
    Run tests on my app
    '''

    def setUp(self):
        '''
        Execute before each test
        '''
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        '''
        Executed after each test
        '''
        pass

    def test_index(self):
        '''
        Test landing page
        '''
        response = self.app.get('/',follow_redirects = True)
        self.assertIn(b'About', response.data)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()
