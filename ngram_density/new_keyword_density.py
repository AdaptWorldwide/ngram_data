from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from collections import Counter
import requests
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup

def grab_words(url):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    r = requests.get(url)
    cleaned_html = cleaner.clean_html(r.text)
    soup = BeautifulSoup(cleaned_html,'html.parser')
    body_text = soup.find('body').get_text()
    return body_text.lower()

def words_keywords(text,keyword_string):
    keyword_string = keyword_string.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    word_count = len(tokens)

    keyword_len = tokenizer.tokenize(keyword_string)
    keyword_len = len(keyword_len)

    our_grams = ngrams(tokens, keyword_len)

    our_results = []

    for item in our_grams:
        item = ' '.join(item)
        our_results.append(item)

    occurences = our_results.count(keyword_string)

    density = ((occurences * keyword_len) / word_count)

    return density, occurences, word_count

