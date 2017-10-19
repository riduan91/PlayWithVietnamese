# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:30:40 2017

@author: ndoannguyen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:33:56 2017

@author: ndoannguyen
"""

import re, requests, time, urllib
from bs4 import BeautifulSoup

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)

from Word import Word

WORD_FILE = "../../BasicData/AllPureVietnameseWords.txt"
SYLLABLE_FILE = "../../BasicData/AllPureVietnameseSyllables.txt"
SINO_VNESE_DICTIONARY_FILE = "../../BasicData/AllSinoVietnameseSyllablesWithMeaning.txt"
SINO_VNESE_CHARACTER_FILE = "../../BasicData/AllSinoVietnameseSyllables.txt"
SINO_VNESE_CLASSIFIED_WORD_FILE = "../../BasicData/SinoVneseClassifiedWords.txt"

def ask_sinovietnamese_word(word):

    r = requests.get('http://hvdic.thivien.net/hv/' + urllib.quote_plus(word))
    soup = BeautifulSoup(r.text)
    paragraphs = soup.findAll('div',{'class':'hvres'})
    
    meanings = {}
    for paragraph in paragraphs:
        try:
            simple = clean(paragraph.find('p', {'class': 'hvres-info small' }).text).encode('latin-1').decode('utf-8')
            if simple.find(u'giản thể') >= 0:
                hanzi = clean(paragraph.find('div', {'class': 'hvres-word han' }).text.encode('latin-1').decode('utf-8'))
                meaning_source = clean(paragraph.find('p', {'class': 'hvres-source'}).text.encode('latin-1').decode('utf-8'))
                if meaning_source.find(u'phổ thông') >= 0:
                    meaning = clean(paragraph.find('div', {'class': 'hvres-meaning han-clickable'}).text.encode('latin-1').decode('utf-8'))                    
                    meanings[hanzi] = meaning
        except:
            pass

    return meanings

def clean(word):
    word = re.sub('\n ', '', word)
    word = re.sub(' \n', '', word)
    word = re.sub('\r', '', word)
    word = re.sub(' {2,}', '', word)
    word = re.sub('\n{2,}', '', word)
    word = re.sub('\n', '     ', word)
    return word

def create_sinovietnamese_dictionary():
    f = open(SYLLABLE_FILE, 'r')
    syllables = f.read().split('\n')
    output = open(SINO_VNESE_DICTIONARY_FILE, 'w')
    for syllable in syllables:
        print "Handling", syllable
        my_dict = ask_sinovietnamese_word(syllable)
        for (k, V) in my_dict.items():
            try:
                output.write("%s\t%s\t%s\n" % (syllable, k.encode('utf-8'), V.encode('utf-8')))
            except:
                pass
    output.close()
    f.close()

def retrieve_sinovietnamese_syllables():
    f = open(SINO_VNESE_DICTIONARY_FILE, 'r')
    lines = f.read().split('\n')
    syllables = set()
    for line in lines:
        elements = line.split('\t')
        syllable = elements[0]
        if len(syllable):
            syllables.add(syllable)
    f.close()
    output = open(SINO_VNESE_CHARACTER_FILE, 'w')
    for syllable in sorted(list(syllables)):
        output.write("%s\n" % syllable)
    output.close()
    return syllables

def classify_sinovietnamese_words():
    f = open(WORD_FILE, 'r')
    lines = f.read().split('\n')
    sinovnese_syllables = retrieve_sinovietnamese_syllables()
    words = {}
    for line in lines:
        if len(line) == 0:
            continue
        word = Word(line)
        word_syllables = word.getSyllables()
        sino_vietnamese = True
        for syllable in word_syllables:
            if syllable.getSyllable() not in sinovnese_syllables:
                sino_vietnamese = False
        if sino_vietnamese:
            words[line] = 1
        else:
            words[line] = 0
    f.close()
    output = open(SINO_VNESE_CLASSIFIED_WORD_FILE, 'w')
    for (k, V) in sorted(words.items()):
        output.write("%s\t%d\n" % (k, V))
    output.close()
    return words
        
            
#print ask_sinovietnamese_word('bác')
print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
#create_sinovietnamese_dictionary()
classify_sinovietnamese_words()
print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())