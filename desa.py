#!/usr/bin/env python3

"""
Sample isolated crawler for
Desa CIMACAN
"""
# Import sys as workaround for module path
import sys
sys.path.insert(0, '/Users/Gandhi/Documents/GitHub/Sideka')

# Import tokenizer
import nltk
from nltk.tokenize import RegexpTokenizer

# Import math and pprint
import math
from pprint import pprint

# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Import Crawler (it resides in "Sideka" dir)
from crawler import Crawler

class Desa(Crawler):

    # Object properties
    def __init__(self):
        self.article_links = []
        self.article = []

    # Override web_login method of the parent Crawler class
    def web_login(self, url, wait_time):
        print("making web request...")
        self.browser.get(url)
        timeout = wait_time
        try:
            WebDriverWait(self.browser, timeout).\
                until(EC.visibility_of_element_located((By.XPATH,
                    '*//div[@class="mh-main-nav-wrap"]'))
                )
            print('webpage opened!')
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.browser.quit()
            pass

    # Get article body
    def get_article_body(self, url, wait_time):
        print("making web request...")
        self.browser.get(url)
        timeout = wait_time
        try:
            print("getting article text")
            WebDriverWait(self.browser, timeout).\
                until(EC.visibility_of_element_located((By.XPATH,
                    '*//div[@class="mh-main-nav-wrap"]'))
                )
            print('webpage opened!')
            article_body = self.browser.find_elements_by_xpath('//article//div[@class="entry-content clearfix"]//p')
            self.article = [item.text for item in article_body]
            return self.article
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.browser.quit()
            pass

    # Go through article pages
    def go_to_article_containers(self, wait_time):
        print("Getting the article pages list...")
        article_page = self.browser.find_element_by_xpath('//div[@class="menu-menu-1-container"]/ul[@id="menu-menu-1"]/li[contains(@class,"menu-item-type-taxonomy")]')
        article_page.click()
        timeout = wait_time
        try:
            WebDriverWait(self.browser, timeout).\
                until(EC.visibility_of_element_located((By.XPATH,
                    '//div[@class="mh-copyright-wrap"]'))
                )
            print('article page opened!')
            article_container = self.browser.find_elements_by_xpath('//h3[@class="entry-title mh-loop-title"]//a[@href]')
            self.article_links = [item.get_attribute("href") for item in article_container]
            return self.article_links
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.browser.quit()
            pass

# Function to plot word freq
def plot_word_freq(text):
    # Create tokenizer: tokenizer
    tokenizer = RegexpTokenizer('\w+')
    # Create tokens from text using tokenize() method: tokens
    tokens = tokenizer.tokenize(text)
    # Initialize new list: words
    words = []
    # Loop through list tokens and make them all lower case
    for word in tokens:
        words.append(word.lower())
    # Get English stopwords into a list: sw
    sw = nltk.corpus.stopwords.words('indonesian')            
    # Initialize new list to contain 'tokens' sans the stopwords: words_ns
    words_ns = []
    # Add to words_ns all words that are in words but not in sw
    for word in words:
        if word not in sw:
            words_ns.append(word)
    # Create freq dist and plot
    freqdist1 = nltk.FreqDist(words_ns)
    freqdist1.plot(25)

# Function to tokenize document: tokenizer
def tokenizer(doc):
    tokenized_doc = [item.lower() for item in doc]
    all_tokens_set = set(tokenized_doc)
    return tokenized_doc, all_tokens_set

# Function to calculate TF: term_frequency
def term_frequency(term, tokenized_doc):
    return tokenized_doc.count(term)

# Function to calculate IDF: inverse_document_frequencies
def inverse_document_frequencies(tokenized_doc, all_tokens_set):
    idf_values = {}
    for token in all_tokens_set:
        contains_token = map(lambda doc: token in doc, tokenized_doc)
        idf_values[token] = 1 + math.log(len(tokenized_doc)/(sum(contains_token)))
    return idf_values

# Instantiate Cimacan 
url = 'http://cimacan.desa.id'
cimacan = Desa()
cimacan.start_driver('../chromedriver')
cimacan.web_login(url, 15)
links = cimacan.go_to_article_containers(15)

# Try to loop links and get the article body
all_article = []
for url in links:
    test_body = cimacan.get_article_body(url, 30)
    all_article.append(test_body)

# Join all articles into one big article
all_article_pre = [item for sublist in all_article
                   for item in sublist]
all_article_pre_cleaned = ' '.join(all_article_pre).replace(',','').replace('.','').\
                            replace('(','').replace(')','').replace(':','').replace('"','').split()

# Checkpoint
#print(all_article_pre)
print(all_article_pre_cleaned)
all_article_fin = ' '.join(all_article_pre_cleaned)

print('-----------' * 10)
print('### ALL ARTICLES ###')
print(all_article_fin)

print('-----------' * 10)

# print article links
print('### ARTICLE LINKS ###')
print(links)

# Close the driver
print('-----------' * 10)
cimacan.close_driver()

# Plot the word distribution
#plot_word_freq(all_article_fin)

# Tokenize doc
tokenized_doc, all_tokens_set = tokenizer(all_article_pre_cleaned)

# Calculate the IDF
idf_values = inverse_document_frequencies(tokenized_doc, all_tokens_set)

# Try to print out TF of term 'rajut'
print(term_frequency('rajut', tokenized_doc))

# Print out the idf_values
pprint(idf_values)
