from lxml.html.clean import Cleaner
import requests
from bs4 import BeautifulSoup
from nltk.util import ngrams
from nltk import word_tokenize
from random import choice

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
 
def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

class Similar():

    def __init__(self):
        self.n_values = [2, 3, 4, 5]
        self.common_punct = ['?','.',':','!','"',"'",',']

    def remove_punct(self,text):
        new_text = text
        for item in self.common_punct:
            new_text = new_text.replace(item, '')
        return new_text

    def get_ngrams(self, text, n):
        text = self.remove_punct(text)
        n_grams = ngrams(word_tokenize(text), n)
        return [' '.join(grams) for grams in n_grams]

    def check_difference(self, n, a, b):
        token_count_a = len(a) * n
        token_count_b = len(b) * n
        duplicate_count = 0
        for token in a:
            if token in b:
                duplicate_count += 1
        return (duplicate_count * n) / token_count_b

    def cleanHTML(self, response):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        html = response.text
        new_html = cleaner.clean_html(html)
        soup = BeautifulSoup(new_html,'html.parser')
        body = soup.find('body').get_text()
        return body

    def action(self, url1, url2):
        url1 = requests.get(url1,headers=random_headers())
        url2 = requests.get(url2,headers=random_headers())
        text1 = self.cleanHTML(url1)
        text2 = self.cleanHTML(url2)
        i = 0
        scores = []
        while i < len(self.n_values):
            current_n = i + 2
            tokens1 = self.get_ngrams(text1,current_n)
            tokens2 = self.get_ngrams(text2,current_n)
            similar_score = self.check_difference(current_n, tokens1, tokens2)
            scores.append(similar_score)
            i += 1
        return scores


#s = Similar()
#a = s.action('http://www.adaptworldwide.com/','http://www.adaptworldwide.com/who-are-we/')
#print(a)


