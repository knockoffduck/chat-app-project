import unittest
from website import create_app, db



# Import your test classes here
from tests.signup import RegistrationTestCase
from tests.login import LoginTestCase
from tests.chat import ChatModelTestCase
from tests.editprofile import EditProfileTestCase

# Add other test classes as needed
def create_test_suite():
    test_suite = unittest.TestSuite()
    
    # Add your test classes to the test suite
    test_suite.addTest(unittest.makeSuite(RegistrationTestCase))
    test_suite.addTest(unittest.makeSuite(LoginTestCase))
    test_suite.addTest(unittest.makeSuite(ChatModelTestCase))
    test_suite.addTest(unittest.makeSuite(EditProfileTestCase))
    # Add other test classes as needed
    
    return test_suite
if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
    # Create the test suite
    test_suite = create_test_suite()
    
    # Create a test runner and run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    
    # Return the test result status
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)
