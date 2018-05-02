#!/usr/bin/env python4

"""
Sideka crawler
"""

# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Import Crawler
from crawler import Crawler

class Sideka(Crawler):

    def __init__(self):
        self.url_to_crawl = 'https://monitor.sideka.id/statistics'
        self.desa_domain = []
        self.desa_berita_rank = []

    # Override web_login() of parent Crawler class
    def web_login(self, url, wait_time):
        print("making web request...")
        self.browser.get(url)
        timeout = wait_time
        try:
            WebDriverWait(self.browser, timeout).\
                until(EC.visibility_of_element_located((By.XPATH,
                    '*//table[@class="htCore"]'))
                )
            print('webpage opened!')
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.browser.quit()
            pass

    # Grab desa URLs
    def grab_desa_urls(self):
        print("Grabbing list of Desa URLS...")
        table_content = self.browser.find_element_by_xpath('*//table[@class="htCore"]')
        desa_container = table_content.text.split()
        self.desa_domain = [item for item in desa_container
                            if '.desa.id' in item]

    # Get the page and parse
    def get_page_and_parse(self, webdriver_path, wait_time):
        self.start_driver(webdriver_path)
        self.web_login(self.url_to_crawl, wait_time)
        self.grab_desa_urls()
        self.close_driver()

        return self.desa_domain

# Class instantiation for Sideka
sideka = Sideka()

# Actually login to sideka webpage
webdriver_path = './chromedriver'
desa_web = sideka.get_page_and_parse(webdriver_path, 30)

# Test print url
print(desa_web)