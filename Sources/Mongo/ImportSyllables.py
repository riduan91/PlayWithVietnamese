# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:49:44 2017

@author: ndoannguyen
"""

BASIC_DATA_DIR = "../../BasicData/"
BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Syllable import Syllable
import Constants

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
SyllableCollection = VietnameseDB['Syllables']

PURE_VNESE_SYLLABLES_FILE_NAME = Constants.PURE_VNESE_SYLLABLES_FILE_NAME

index = 1

for line in open(BASIC_DATA_DIR + PURE_VNESE_SYLLABLES_FILE_NAME):
    line = line.replace("\n", "").replace("\r", "")
    syllable = Syllable(line)
    mongo_document = {
                        "_id": "SYL" + str(index).zfill(5),
                        "syllable" : syllable.getSyllable(),
                        "beginning_consonant": syllable.getBeginningConsonant(),
                        "accent" : syllable.getAccent(),
                        "rhyme" : syllable.getRhyme().getRhyme(),
                        "secondary_part" : syllable.getRhyme().getSecondaryPart(),
                        "primary_part" : syllable.getRhyme().getPrimaryPart(),
                        "end_part" : syllable.getRhyme().getEndPart()
                    }
    index += 1
    try:
        SyllableCollection.insert_one(mongo_document)
    except DuplicateKeyError:
        print "[Error] Syllable with id %s already exists." % ("SYL" + str(index).zfill(5))