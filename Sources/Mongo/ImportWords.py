# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:59:17 2017

@author: ndoannguyen
2 mins to run
"""

"""
This import words from frequency file into mongo
"""

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Word import Word
import Constants

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
WordCollection = VietnameseDB['Words']
RhymeCollection = VietnameseDB['Rhymes']

BASIC_DATA_DIR = Constants.BASIC_DATA_DIR
PURE_VNESE_WORDS_FILE_NAME = Constants.PURE_VNESE_WORDS_FILE_NAME
FREQUENCY_OF_WORD_FILE_NAME = Constants.FREQUENCY_OF_WORD_FILE_NAME

def ImportWords(frequency_file_name, word_collection_name):
    WordCollection = VietnameseDB[word_collection_name]
    index = 1
    for line in open(frequency_file_name):
        line = line.replace("\n", "").replace("\r", "")
        word_fred = line.split("\t")
        word, fred = Word(word_fred[0]), int(word_fred[1])
        quasi_rhymable_rhymes = RhymeCollection.find_one({"rhyme": word.getRhyme().getRhyme()})['quasi_rhymable_rhymes']
    
        accent_type = 1
        if word.getAccent() in 'zf':
            accent_type = 0
        
        word_mongo_document = {
                            "_id": "WOR" + str(index).zfill(5),
                            "word" : word.getWord(),
                            "syllables" : [syllable.getSyllable() for syllable in word.getSyllables()],
                                           "length" : word.getLength(),
                            "rhyme" : word.getRhyme().getRhyme(),
                            "accent" : word.getAccent(),
                            "accent_type" : accent_type,
                            "quasi_rhymable_rhymes" : quasi_rhymable_rhymes,
                            "popularity" : fred
                            }
        try:
            WordCollection.insert_one(word_mongo_document)
            index += 1
        except DuplicateKeyError:
            print "[Error] Word with id %s already exists." % ("RHY" + str(index).zfill(5))
            index += 1

ImportWords(BASIC_DATA_DIR + FREQUENCY_OF_WORD_FILE_NAME, 'Words')
#ImportWords(BASIC_DATA_DIR + "Statistics_TruyenKieu.txt", 'WordsInTruyenKieu')
