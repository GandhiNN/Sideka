#!/usr/local/bin/python3

import requests
import re
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup

# Set default plot styling
sns.set()

# Function to plot word freq
def plot_word_freq(url):
    """Takes a URL of 'desa': still STATIC"""

    # Make the request and create the response object: response
    response = requests.get(url)

    # Extract HTML texts contained in Response object: html
    html = response.text

    # Create a BeautifulSoup object from the HTML: soup
    soup = BeautifulSoup(html, "html5lib")

    # Get the text out of the soup: text
    text = soup.get_text()

    # Re-encode the string so as to retain only the ASCII characters (and ignore the others)
    # and then decode again
    text = text.encode('ascii', 'ignore').decode('ascii')
    
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
    
    # <!-- comment out plotting function first -->
    #freqdist1.plot(25)

    return text

# Define URL 
url_desa = 'http://tohe.desa.id/2018/04/27/siswa-siswi-smpn-satap-wetear-sukses-akhiri-ujian-nasional-hari-ini-dengan-seragam-dan-kain-tenun/'

# Plot word frequency
html_source = plot_word_freq(url_desa)
print(html_source)

