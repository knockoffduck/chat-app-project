import unittest
from selenium import webdriver

class ChatAppSeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  

    def tearDown(self):
        self.driver.quit()

    def test_chat_functionality(self):
        # open web
        self.driver.get('http://127.0.0.1:5000')

        # login
        email_input = self.driver.find_element_by_id('email-input')
        email_input.send_keys('your-email@example.com')

        password_input = self.driver.find_element_by_id('password-input')
        password_input.send_keys('your-password')

        login_button = self.driver.find_element_by_id('login-button')
        login_button.click()

        # display test
        chat_messages = self.driver.find_elements_by_class_name('chat-message')
        self.assertEqual(len(chat_messages), 0)  # check initial chat len = 0

        # send mess
        message_input = self.driver.find_element_by_id('message-input')
        message_input.send_keys('Hello, this is my test message')

        send_button = self.driver.find_element_by_id('send-button')
        send_button.click()

        # test display mess
        chat_messages = self.driver.find_elements_by_class_name('chat-message')
        self.assertEqual(len(chat_messages), 1)  # there is 1 line mess

        # test chat body
        message_content = chat_messages[0].text
        self.assertEqual(message_content, 'Hello, this is my test message')  # correct display

if __name__ == '__main__':
    unittest.main()
