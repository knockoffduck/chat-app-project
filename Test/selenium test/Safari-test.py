import os
import sys

# Get the parent directory (root directory of the project)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

import unittest, os, time, datetime
from selenium import webdriver
from website import create_app, db
from website.models import User, Chat
from config import Config, TestingConfig, basedir
from selenium.webdriver.common.by import By

class SystemTest(unittest.TestCase):
  driver = None
  service = None
  
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.driver = webdriver.Safari()
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
      db.session.query(User).delete()
      db.session.commit()
      db.session.remove()


  def test_register(self):
    u = User.query.filter_by(email='test@email.net').first()
    self.assertEqual(u.firstname,'Bob',msg='user exists in db')
    self.driver.get('http://localhost:5000/auth/signup')
    self.driver.implicitly_wait(5)
    fname = self.driver.find_element(By.ID, "first_name")
    fname.send_keys('Kelly')
    lname = self.driver.find_element(By.ID, "last_name")
    lname.send_keys('Smith')
    email = self.driver.find_element(By.ID, "email")
    email.send_keys('hi@gmail.com')
    pword = self.driver.find_element(By.ID, "password")
    pword.send_keys('hello')
    pword2 = self.driver.find_element(By.ID, "confirm_password")
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
  unittest.main(verbosity=2)