# import unittest

# test_loader = unittest.TestLoader()
# test_suite = test_loader.discover(start_dir='tests', pattern='test*.py')
# unittest.TextTestRunner(verbosity=2).run(test_suite)


import unittest
from tests.unit.test_unit import UserModelCase
from tests.functional.test_routes import RouteTestCase

# Create a TestSuite and add all test cases
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(UserModelCase))
suite.addTest(unittest.makeSuite(RouteTestCase))

# Create a TestRunner and run the TestSuite
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
