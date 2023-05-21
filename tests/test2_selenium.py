import os

import sys




# Get the parent directory (root directory of the project)

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# Add the parent directory to the Python path

sys.path.append(parent_dir)




import unittest, os, time, datetime, tracemalloc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from website import create_app, db
from website.models import User, Chat
from config import TestingConfig




from selenium.webdriver.chrome.service import Service




class SystemTest(unittest.TestCase):
    driver = None
    service = None




@classmethod
def setUpClass(cls):
    cls.service = Service(executable_path='drivers/chromedriver')

def setUp(self):

   self.app = create_app(TestingConfig)

   self.client = self.app.test_client()

   self.driver = webdriver.Chrome(service=self.service)

   with self.app.app_context():

     db.create_all()

     u1 = User(firstname='Bob',lastname='Test',

               dob=datetime.datetime(2020,1,2),country="Aus",gender="Other")

     u1.set_password('password')

     u1.set_email('test@email.net.au')

     db.session.add(u1)

     db.session.commit()

     self.driver.maximize_window()

     self.driver.get('http://localhost:5000/')

   if not self.driver:

     self.skipTest("Web browser not available")



def tearDown(self):

   if self.driver:

       self.driver.close()




       with self.app.app_context():

           db.session.query(User).delete()

           db.session.query(Chat).delete()

           db.session.commit()

           db.session.remove()




       self.driver.quit()




   if self.service:

       self.service.stop()




def test_register(self):
    self.driver.get('http://localhost:5000/auth/signup')
    self.driver.implicitly_wait(5)
    fname = self.driver.find_element(By.ID, "firstname")
    fname.click()
    time.sleep(1)
    self.driver.implicitly_wait(5)
    fname.send_keys('Kelly')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    lname = self.driver.find_element(By.ID, "lastname")
    lname.click()
    time.sleep(1)
    self.driver.implicitly_wait(5)
    lname.send_keys('Smith')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    email = self.driver.find_element(By.ID, "email")
    email.click()
    time.sleep(1)
    self.driver.implicitly_wait(5)
    email.send_keys('q@gmail.com')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    pword = self.driver.find_element(By.ID, "password")
    pword.click()
    time.sleep(1)
    self.driver.implicitly_wait(5)
    pword.send_keys('hello')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    pword2 = self.driver.find_element(By.ID, "password2")
    pword2.click()
    pword2.send_keys('hello')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    dob = self.driver.find_element(By.ID, "dob")
    dob.click()
    dob.send_keys("1999-01-01")
    time.sleep(1)
    self.driver.implicitly_wait(5)
    country = self.driver.find_element(By.ID, "country")
    country.click()
    country.send_keys('Aus')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    gender = self.driver.find_element(By.ID, "gender")
    gender.click()
    gender.send_keys('Female')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    submit = self.driver.find_element(By.ID, "submit")
    submit.click()
    u = User.query.filter_by(email='q@gmail.com').first()
    self.assertEqual(u.email,'q@gmail.com', msg='user exists in db')

if __name__=='__main__':
    tracemalloc.start()
    unittest.main(verbosity=2)
