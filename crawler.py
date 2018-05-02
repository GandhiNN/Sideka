#!/usr/bin/env python3

"""
1.Create a class for crawler which:
- has an extendable login() and parse()-like method;
"""

# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Crawler():

    """Blueprint for crawler"""

    # Open webdriver object
    def start_driver(self, exec_path):
        self.option = webdriver.ChromeOptions().add_argument(" - incognito")
        self.exec_path = exec_path
        webdriver_name = self.exec_path.split("/")[-1]
        print("starting {} webdriver...".format(webdriver_name))
        self.browser = webdriver.Chrome(executable_path=self.exec_path,
            chrome_options=self.option)

    # Close webdriver object
    def close_driver(self):
        print("closing driver...")
        self.browser.quit()
        print("driver closed!")

    # Login function
    def web_login(self, url):
        print("making web request...")
        print("getting pass the login page...")

    # Grab items
    def grab_items(self):
        print("grabbing list of items...")

