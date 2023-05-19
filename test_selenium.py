import unittest, os, time, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website import create_app, db
from website.models import User, Chat
from config import Config, TestingConfig, basedir


class SystemTest(unittest.TestCase):
  driver = None
  
  def setUp(self):

    self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'drivers/chromedriver'))

    if not self.driver:
      self.skipTest('Web browser not available')
    else:
      db.init_app(create_app)
      db.create_all()
      u1 = User(firstname='Bob',lastname='Test',email='test@email.net',dob=datetime.datetime(2020,1,2),country="Aus",gender="Other")
      u1.set_password('password')
      db.session.add(u1)
      db.session.commit()
      self.driver.maximize_window()
      self.driver.get('http://localhost:5000/')

  def tearDown(self):
    if self.driver:
      self.driver.close()
      db.session.query(User).delete()
      db.session.commit()
      db.session.remove()


  def test_register(self):
    u = User.query.filter_by(email='e@email.com').first()
    self.assertEqual(u.firstname,'Bob',msg='user exists in db')
    self.driver.get('http://localhost:5000/auth/signup')
    self.driver.implicitly_wait(5)
    fname = self.driver.find_element_by_id('firstname')
    fname.send_keys('Kelly')
    lname = self.driver.find_element_by_id('lastname')
    lname.send_keys('Smith')
    email = self.driver.find_element_by_id('email')
    email.send_keys('hi@gmail.com')
    pword = self.driver.find_element_by_id('password')
    pword.send_keys('hello')
    pword2 = self.driver.find_element_by_id('password2')
    pword2.send_keys('hello')
    dob = self.driver.find_element_by_id('dob')
    dob.send_keys(datetime.datetime(1999,1,1))
    country = self.driver.find_element_by_id('country')
    country.send_keys('Aus')
    gender = self.driver.find_element_by_id('gender')
    gender.send_keys('Female')
    time.sleep(1)
    self.driver.implicitly_wait(5)
    submit = self.driver.find_element_by_id('submit')
    submit.click()
    #check login success
    # self.driver.implicitly_wait(5)
    # time.sleep(1)
    # logout = self.driver.find_element_by_partial_link_text('Logout')
    # self.assertEqual(logout.get_attribute('innerHTML'), 'Logout Testy', msg='Logged in')


if __name__=='__main__':
  unittest.main(verbosity=2)