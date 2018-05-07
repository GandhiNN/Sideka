#!/usr/bin/env/python3

# Import required packages
import glob
import nltk
import operator
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from string import punctuation
from pprint import pprint

## PREPROCESS Corpora
## Load all articles, and clean it as much as we can

# Load 'scraped' article body
source_dir = 'pejeng_articles/'

# Load the news articles: articles
file_list = glob.glob(source_dir + '*.txt')
articles = [open(f, 'r').read() for f in file_list]

# Preprocess articles: lowercasing and tokenizing all words
articles_lower_tokenize = [word_tokenize(t.lower())
                           for t in articles]

# Preprocess articles: removing 'indonesian' stopwords: articles_no_stop
stopwords_indonesian = stopwords.words('indonesian')
articles_no_stop = [[t for t in sublist if t not in stopwords_indonesian]
                    for sublist in articles_lower_tokenize]

# Preprocess articles: removing punctuation
articles_no_empty = [[t for t in sublist if t]
                     for sublist in articles_no_stop]
articles_no_empty_intermediate_1 = [[t for t in sublist if '``' not in t]
                                    for sublist in articles_no_empty]
articles_no_empty_intermediate_2 = [[t for t in sublist if '\'\'' not in t]
                                    for sublist in articles_no_empty_intermediate_1]
articles_cleaned = [[t for t in sublist if t not in punctuation]
                    for sublist in articles_no_empty_intermediate_2]
print(len(articles_cleaned))

## Simple BAG-OF-WORDS Model
## Looking up top 5 most-common words in the corpora

# Create a counter object: counter
counter = Counter([word for words in articles_cleaned for word in set(words)])
print('-----' * 8)
print("Top 10 Words according to frequency:")
print('-----' * 8)
print(counter.most_common(10), '\n')

## TF-IDF Using Gensim
# Create a gensim corpus and then apply Tfidf to that corpus
from gensim.corpora.dictionary import Dictionary

# Create a (gensim) dictionary object from the articles_cleaned: dictionary
dictionary = Dictionary(articles_cleaned)

# Create a gensim corpus
corpus = [dictionary.doc2bow(article) for article in articles_cleaned]

# Import TfidfModel from gensim
from gensim.models.tfidfmodel import TfidfModel

# Create a tfidf object from corpus
tfidf = TfidfModel(corpus)
print('-----' * 8)
print("TF-IDF Object from Corpus")
print('-----' * 8)
print(tfidf, '\n')

# Checkpoint, print articles_cleaned
print('-----' * 8)
print("Cleaned Articles:")
print('-----' * 8)
print(articles_cleaned[0], '\n')

# Check the tfidf weight in the first document of corpus
# corpus[1] = articles_cleaned[1]
print('-----' * 8)
print('TF-IDF for the first document in the corpus')
print('-----' * 8)
print(tfidf[corpus[1]], '\n')

# Test: getting the word inside a doc and its tf-idf weight
doc = corpus[1]
tfidf_weights = tfidf[doc]

# Sort the weights from highest to lowest: sorted_tfidf_weights
sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)

# Print the top 5 weighted words of doc
print('-----' * 8)
print('Top 5 Weighted Words for corpus[1]')
print('-----' * 8)
for term_id, weight in sorted_tfidf_weights[:5]:
    print(dictionary.get(term_id), weight)

# Get the TFIDF Weights of all terms found in corpus
#  print as list of tuples, in descending order 
print('\n')

# Create a container for the list of tuples: tfidf_tuples
tfidf_tuples = []

# Loop over the cleaned articles
# Get the top-5 of tfidf weight
for i in range(len(articles_cleaned)):
    doc = corpus[i]
    tfidf_weights = tfidf[doc]
    sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
    for term_id, weight in sorted_tfidf_weights[:5]:
        tfidf_tuples.append((dictionary.get(term_id), weight))

# Sort the tfidif_tuples based on weight
tfidf_tuples.sort(key=operator.itemgetter(1), reverse=True)
print('-----' * 8)
print('Term and Weight for entire corpora')
print('-----' * 8)
pprint(tfidf_tuples)

# Write results to csv
with open('tfidf_pejeng.csv', 'w') as f_out:
    csv_out = csv.writer(f_out)
    csv_out.writerow(['term', 'term_id', 'weight', 'corpus_id'])
    for row in tfidf_tuples:
        csv_out.writerow(row)
