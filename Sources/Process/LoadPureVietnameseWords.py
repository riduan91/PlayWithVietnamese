# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 17:12:33 2017

@author: ndoannguyen
"""

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)

from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
WordCollection = VietnameseDB['Words']

PURE_VNESE_WORDS = [word['word'] for word in WordCollection.find({}, {"_id":0, "word":1})]