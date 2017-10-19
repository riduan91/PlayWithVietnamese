# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:34:54 2017

@author: ndoannguyen
"""

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
import Constants
from Word import Word

BASIC_DATA_DIR = Constants.BASIC_DATA_DIR
RAW_WORDS_FILE_NAME = Constants.RAW_WORDS_FILE_NAME
PURE_VNESE_SYLLABLES_FILE_NAME = Constants.PURE_VNESE_SYLLABLES_FILE_NAME

raw_words_text_file = BASIC_DATA_DIR + RAW_WORDS_FILE_NAME

pure_vnese_syllable_collection = {}

for line in open(raw_words_text_file):
    line = line.replace("\n", "")
    word = Word(line)
    syllables = word.getSyllables()
    for syllable in syllables:
        syllable_text = syllable.getSyllable()
        if syllable.isPureVietnameseSyllable() and not pure_vnese_syllable_collection.has_key(syllable_text) :
            pure_vnese_syllable_collection[syllable_text] = 1

pure_vnese_syllables_text_file = open(BASIC_DATA_DIR + PURE_VNESE_SYLLABLES_FILE_NAME, 'w')
print BASIC_DATA_DIR + PURE_VNESE_SYLLABLES_FILE_NAME
for word in sorted(pure_vnese_syllable_collection.keys()):
    pure_vnese_syllables_text_file.write(word + "\n")

pure_vnese_syllables_text_file.close()