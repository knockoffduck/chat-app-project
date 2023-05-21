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
        cls.service = Service(executable_path="drivers/chromedriver")

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.driver = webdriver.Chrome(service=self.service)
        with self.app.app_context():
            db.create_all()
            u1 = User(
                firstname="Bob",
                lastname="Test",
                dob=datetime.datetime(2020, 1, 2),
                country="Aus",
                gender="Other",
            )
            u1.set_password("password")
            u1.set_email("test@email.net.au")
            db.session.add(u1)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get("http://localhost:5000/")
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
        self.driver.get("http://localhost:5000/auth/signup")
        self.driver.implicitly_wait(5)
        fname = self.driver.find_element(By.ID, "firstname")
        fname.click()
        self.driver.implicitly_wait(5)
        fname.send_keys("Kelly")
        self.driver.implicitly_wait(5)
        lname = self.driver.find_element(By.ID, "lastname")
        lname.click()
        self.driver.implicitly_wait(5)
        lname.send_keys("Smith")
        self.driver.implicitly_wait(5)
        email = self.driver.find_element(By.ID, "email")
        email.click()
        self.driver.implicitly_wait(5)
        email.send_keys("q@gmail.com")
        self.driver.implicitly_wait(5)
        pword = self.driver.find_element(By.ID, "password")
        pword.click()
        self.driver.implicitly_wait(5)
        pword.send_keys("hello")
        self.driver.implicitly_wait(5)
        pword2 = self.driver.find_element(By.ID, "password2")
        pword2.click()
        pword2.send_keys("hello")
        self.driver.implicitly_wait(5)
        dob = self.driver.find_element(By.ID, "dob")
        dob.click()
        dob.send_keys("01/01/2000")
        self.driver.implicitly_wait(5)
        country = self.driver.find_element(By.ID, "country")
        country.click()
        country.send_keys("Aus")
        self.driver.implicitly_wait(5)
        gender = self.driver.find_element(By.ID, "gender")
        gender.click()
        gender.send_keys("Female")
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        u = User.query.filter_by(email="q@gmail.com").first()
        print(User.query.with_entities(User.email).all())
        self.assertEqual(u.email, "q@gmail.com", msg="user exists in db")

    def test_login(self):
        u = User.query.filter_by(email="test@email.net.au").first()
        self.assertEqual(u.email, "test@email.net.au", msg="user exists in db")
        self.driver.get("http://localhost:5000/auth/login")
        self.driver.implicitly_wait(5)
        email = self.driver.find_element(By.ID, "email")
        email.send_keys("test@email.net.au")
        pword = self.driver.find_element(By.ID, "password")
        pword.send_keys("password")
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        assert "Send" in self.driver.page_source

    def test_avatar(self):
        self.driver.get("http://localhost:5000/auth/login")
        self.driver.implicitly_wait(5)
        email = self.driver.find_element(By.ID, "email")
        email.click()
        email.send_keys("test@email.net.au")

        pword = self.driver.find_element(By.ID, "password")
        email.click()
        pword.send_keys("password")
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element(By.ID, "submit")
        submit.submit()
        time.sleep(1)
        self.driver.implicitly_wait(20)
        self.driver.get("http://localhost:5000/account")
        time.sleep(5)

        avatar_input = self.driver.find_element(By.ID, "user_avatar")

        avatar_file = os.path.abspath("../tests/images/Avatar1.jpg")

        avatar_input.send_keys(avatar_file)
        time.sleep(1)
        self.driver.implicitly_wait(5)

        upload_avatar_button = self.driver.find_element(By.ID, "upload-avatar-button")
        upload_avatar_button.click()
        time.sleep(1)
        self.driver.implicitly_wait(5)

    def test_chat_functionality(self):
        # login
        self.driver.get("http://localhost:5000/auth/login")
        self.driver.implicitly_wait(5)
        email = self.driver.find_element(By.ID, "email")
        email.send_keys("test@email.net.au")
        pword = self.driver.find_element(By.ID, "password")
        pword.send_keys("password")
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        time.sleep(1)
        self.driver.implicitly_wait(5)

        # send mess
        message_input = self.driver.find_element(By.ID, "message-input")
        message_input.send_keys("Hello, this is my test message")
        time.sleep(1)
        self.driver.implicitly_wait(5)
        send_button = self.driver.find_element(By.ID, "send-input")
        send_button.click()
        time.sleep(1)
        self.driver.implicitly_wait(5)

        # test display message
        chat_messages = [
            element
            for element in self.driver.find_elements(
                By.CSS_SELECTOR, ".user>.chat-bubble"
            )
        ]
        self.assertEqual(len(chat_messages), 1)  # there is 1 message
        time.sleep(1)
        self.driver.implicitly_wait(5)
        # test chat body
        message_content = chat_messages[0].text
        self.assertEqual(
            message_content, "Hello, this is my test message"
        )  # correct display


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main(verbosity=2)
