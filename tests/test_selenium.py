import os
import sys

# Get the parent directory (root directory of the project)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

import unittest, os, time, datetime, tracemalloc
from selenium import webdriver
from selenium.webdriver.common.by import By
from website import create_app, db
from website.models import User, Chat
from config import basedir, TestingConfig


from selenium.webdriver.chrome.service import Service

class SystemTest(unittest.TestCase):
  driver = None
  service = None
  

  @classmethod
  def setUpClass(cls):
    cls.service = Service(executable_path='path/to/chromedriver')

  
  def setUp(self):
      self.app = create_app(TestingConfig)
      self.client = self.app.test_client()
      self.driver = webdriver.Chrome(service=self.service)
      with self.app.app_context():
        db.create_all()
        u1 = User(firstname='Bob',lastname='Test',email='test@email.net',
                  dob=datetime.datetime(2020,1,2),country="Aus",gender="Other")
        u1.set_password('password')
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
    fname.send_keys('Kelly')
    lname = self.driver.find_element(By.ID, "lastname")
    lname.send_keys('Smith')
    email = self.driver.find_element(By.ID, "email")
    email.send_keys('q@gmail.com')
    pword = self.driver.find_element(By.ID, "password")
    pword.send_keys('hello')
    pword2 = self.driver.find_element(By.ID, "password2")
    pword2.send_keys('hello')
    dob = self.driver.find_element(By.ID, "dob")
    dob.send_keys("1999-01-01")
    country = self.driver.find_element(By.ID, "country")
    country.send_keys('Aus')
    gender = self.driver.find_element(By.ID, "gender")
    gender.send_keys('Female')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    submit = self.driver.find_element(By.ID, "submit")
    submit.click()

  def test_login(self):
    u = User.query.filter_by(email='test@email.net').first()
    self.assertEqual(u.email,'test@email.net', msg='user exists in db')
    self.driver.get('http://localhost:5000/auth/login')
    self.driver.implicitly_wait(5)
    email = self.driver.find_element(By.ID, "email")
    email.send_keys('test@email.net')
    pword = self.driver.find_element(By.ID, "password")
    pword.send_keys('password')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    submit = self.driver.find_element(By.ID, "submit")
    submit.click()
    self.assertEqual(u.email,'test@email.net', msg='logged in')

if __name__=='__main__':
  tracemalloc.start()
  unittest.main(verbosity=2)