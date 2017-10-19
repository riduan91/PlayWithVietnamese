# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:16:33 2017

@author: ndoannguyen
"""

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Word import Word

from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
DefaultWordCollection = VietnameseDB['Words']
RhymeCollection = VietnameseDB['Rhymes']


def findQuasiRhymableWords(word, collection_name, limit = -1):
    """
        Trả lại một MongoCursor
    """
    WordCollection = VietnameseDB[collection_name]
    try:
        corresponding_word = DefaultWordCollection.find_one({"word": word.getWord()})
        quasi_rhymable_rhymes = corresponding_word["quasi_rhymable_rhymes"]
        accent_type = corresponding_word["accent_type"]
        if limit > 0:
            quasi_rhymable_words_cursor = WordCollection.find({"$and": [{"rhyme": {"$in": quasi_rhymable_rhymes}}, {"accent_type": accent_type} ]}).sort("popularity", -1).limit(limit)
        else:
            quasi_rhymable_words_cursor = WordCollection.find({"$and": [{"rhyme": {"$in": quasi_rhymable_rhymes}}, {"accent_type": accent_type} ]}).sort("popularity", -1)
    except TypeError:
        print "[Error] Word \"%s\" not found in dictionary." % word.getWord()
        return None
    return quasi_rhymable_words_cursor