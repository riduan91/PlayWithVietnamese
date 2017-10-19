# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 00:30:13 2017

@author: ndoannguyen
"""

import re
from MakeArticleCorpus import *

DATA_DIR = "../../FrequencyData/"
WORD_FILE = "AllPureVietnameseWords.txt"

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Syllable import Syllable

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".0","<point>0").replace(".1","<point>1").replace(".2","<point>2").replace(".3","<point>3").replace(".4","<point>4")
    text = text.replace(".5","<point>5").replace(".6","<point>6").replace(".7","<point>7").replace(".8","<point>8").replace(".9","<point>9")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    text = text.replace("\xc2\xa0", "")
    sentences = text.split("<stop>")

    sentences = sentences[:-1]
    sentences = [transform_number(s.strip()) for s in sentences]
    return sentences

def transform_number(text):
    text = text.replace("<point>0", ",0").replace("<point>1", ".1").replace("<point>2", ".2").replace("<point>3", ".3").replace("<point>4", ".4")
    text = text.replace("<point>5", ".5").replace("<point>6", ".6").replace("<point>7", ".7").replace("<point>8", ".8").replace("<point>9", ".9")
    return text

def splitDataToSentences(datafile):
    f = open(DATA_DIR + datafile, 'r')
    data = f.read()
    data = data.replace("\n\n\n", "\n\n\n\n")
    paragraphs = data.split("\n\n")
    sentences = []
    for paragraph in paragraphs:
        sentences += split_into_sentences(paragraph)
    f.close()
    return sentences

def cleanSentence(sentence):
    sentence = re.sub(' +', ' ', sentence)
    if len(sentence) > 0 and sentence[0] == ' ':
        sentence = sentence[1:]
    if len(sentence) > 0 and sentence[-1] == ' ':
        sentence = sentence[:-1]
    return sentence
    
def storeSentencesToFile(sentences, filename):
    f = open(DATA_DIR + filename, 'w')
    for sentence in sentences:
        if sentence != '.':
            f.write(sentence + '\n')
    f.close()

def load_words(filename):
    f = open(DATA_DIR + filename, 'r')
    frequency = {}
    words = f.read().split("\n")
    for word in words:
        frequency[word] = 0
    f.close()
    return frequency
    
def clean_sentence(sentence):
    pattern = re.compile(r'[,;\'\"\:\-]')
    sentence = pattern.sub("", sentence)
    return sentence

def split_sentence_into_parts(sentence):
    parts = re.split(r'[,\:\-\.{1,}\?\!]\s*', sentence)
    return parts

def split_part_into_syllables(part):
    syllable_list = []
    pattern = re.compile(r'[\"\'\(\)\/\@\*\&\%\“]')
    if len(part) > 0:
        syllables = part.split(' ')
        for syllable in syllables:
            syllable = pattern.sub('', syllable)
            Syl = Syllable(syllable)
            syllable = Syl.getSyllable()
            if len(syllable) > 0:
                syllable_list.append(syllable)
    return syllable_list

def split_part_into_words(part, dictionary, sub_dictionary):
    syllables = split_part_into_syllables(part)
    n = len(syllables)
    current_position = 0
    while current_position < n:
        for i in range(4, -1, -1):
            pre_word = " ".join(syllables[current_position: current_position + i])
            if pre_word in dictionary.keys():
                if pre_word not in sub_dictionary:
                    sub_dictionary[pre_word] = 1
                else:
                    sub_dictionary[pre_word] += 1
                current_position += i
                break
            if i == 1:
                current_position += i
    return sub_dictionary

def split_sentence_into_words(sentence, dictionary, sub_dictionary):
    parts = split_sentence_into_parts(sentence)
    for part in parts:
        sub_dictionary = split_part_into_words(part, dictionary, sub_dictionary)
    return sub_dictionary
    
def make_words_frequency_corpus(source_file, destination_file, data_file, dictionary_file):
    dictionary = load_words(dictionary_file)
    sub_dictionary = {}
    if source_file != None:
        fs = open(DATA_DIR + source_file, 'r')
        res = fs.read().split("\n")
        for r in res:
            if '\t' in r:
                word, freq = r.split("\t")
                sub_dictionary[word] = int(freq)
        fs.close()
    
    ds = open(DATA_DIR + data_file, 'r')
    res = ds.read().split("\n")
    for sentence in res:
        sub_dictionary = split_sentence_into_words(sentence, dictionary, sub_dictionary)
    ds.close()
    
    rs = open(DATA_DIR + destination_file, 'w')
    for key in sorted(sub_dictionary.keys()):
        rs.write("%s\t%d\n" % (key, sub_dictionary[key]))
    rs.close()
    
    return
    
    
    

#-------MAIN-------

"""
dates = [20170717]
dates_from = [1500242400]
dates_end = [1500325944]


for i in range(len(dates_from)):
    print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    prepare_stockage()
    store_article_url(dates_from[i], dates_end[i], "articles_%d.txt" % dates[i])
    store_articles_content("articles_%d.txt" % dates[i] , "data_%d.txt" % dates[i])
    sentences = splitDataToSentences("data_%d.txt" % dates[i])
    storeSentencesToFile(sentences, "sentences_%d.txt" % dates[i])

for i in range(len(dates_from)):
    make_words_frequency_corpus("Statistics_12-1607.txt", "Statistics_12-1707.txt", "sentences_%d.txt" % dates[i], "AllPureVietnameseWords.txt")
"""

make_words_frequency_corpus("Statistics_Null.txt", "Statistics_TruyenKieu.txt", "TruyenKieu.txt", "AllPureVietnameseWords.txt")