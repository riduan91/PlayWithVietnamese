# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:31:40 2017

@author: ndoannguyen
"""

BASIC_DATA_DIR = "../../BasicData/"
BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Word import Word

RAW_WORDS_FILE_NAME = "AllRawWords.txt"
PURE_VNESE_WORDS_FILE_NAME = "AllPureVietnameseWords.txt"

raw_words_text_file = BASIC_DATA_DIR + RAW_WORDS_FILE_NAME

pure_vnese_word_collection = {}

for line in open(raw_words_text_file):
    line = line.replace("\n", "")
    word = Word(line)
    if word.isPureVietnameseWord() and not pure_vnese_word_collection.has_key(line) :
        pure_vnese_word_collection[line] = 1

pure_vnese_words_text_file = open(BASIC_DATA_DIR + PURE_VNESE_WORDS_FILE_NAME, 'w')
for word in sorted(pure_vnese_word_collection.keys()):
    pure_vnese_words_text_file.write(word + "\n")

pure_vnese_words_text_file.close()