# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:33:56 2017

@author: ndoannguyen
"""
# Get the first 5 hits for "google 1.9.1 python" in Google Pakistan
#
import requests, re
import time
import urllib
from bs4 import BeautifulSoup

from google import search

def ask_from_pos(word, pos):

    r = requests.get('http://www.google.com.vn/search',
            params={'q': '%s' % (urllib.quote(word).replace("%20", "+")), 'start': pos})
    soup = BeautifulSoup(r.text)

    print soup
    text = soup.find('div',{'id':'resultStats'}).text
    if text == "":
        return 0

    text = text.replace('.', '')
    number_list = re.findall(r'\d+', text)
    nb_results = number_list[-1]
    return int(nb_results)

def ask(word):
    sup = presearch_pos(word, 1)
    return search_pos(word, 1, sup)

def search_pos(word, inf, sup):
    med = (inf + sup)/2
    nb_res = ask_from_pos(word, med)
    if (med == inf):        
        return nb_res
    if nb_res > 0:
        inf = (inf + sup)/2
    elif nb_res == 0:
        sup = (inf + sup)/2
    time.sleep(2.0)
    return search_pos(word, inf, sup)
        
def presearch_pos(word, sup):
    nb_res = ask_from_pos(word, sup)
    if nb_res == 0:
        return sup   
    time.sleep(2.0)
    return presearch_pos(word, 2*sup)
    
def count(word):    
    start_pos = 1
    s = search(word, start=start_pos, stop=start_pos+1, pause=0.1)
    while len(list(s)) > 0:
        start_pos *= 2
        s = search(word, start=start_pos, stop=start_pos+1, pause=0.1)
    return start_pos

print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
print "Stopped at", count("\"Hà Nội\"")
print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())