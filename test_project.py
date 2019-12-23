from selenium import webdriver
import unittest
from home_page import HomePage

class TempMailTest(unittest.TestCase):

    def test_open_qr(self):
        self.preconditions()

        hp = HomePage(self.driver)

        hp.open_qr()

        self.postconditions()

    def test_language_change(self):
        self.preconditions()

        hp = HomePage(self.driver)

        hp.language_change()

        self.postconditions()

    def preconditions(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://temp-mail.org/ru/")

    def postconditions(self):
        self.driver.close()
        self.driver.quit()

    # def test_fullpage_screenshot(self):
    #     self.driver = webdriver.Chrome()
    #     driver = self.driver
    #
    #     driver.maximize_window()
    #     driver.get("https://www.google.com/")
    #
    #     hp = HomePage(self.driver)
    #
    #     hp.test_fullpage_screenshot()
    #
    #     driver.close()
    #     driver.quit()
