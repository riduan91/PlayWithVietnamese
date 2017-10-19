# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:31:40 2017

@author: ndoannguyen
"""

import sys
sys.path.append("../Basic/")
sys.path.append("../Configuration/")
from Word import Word
import configuration

raw_words_text_file = configuration.RAW_WORDS_FILE_NAME

pure_vnese_word_collection = {}

for line in open(raw_words_text_file):
    line = line.replace("\n", "")
    word = Word(line)
    if word.isPureVietnameseWord() and not pure_vnese_word_collection.has_key(line) :
        pure_vnese_word_collection[line] = 1

pure_vnese_words_text_file = open(PURE_VNESE_WORDS_FILE_NAME, 'w')
for word in sorted(pure_vnese_word_collection.keys()):
    pure_vnese_words_text_file.write(word + "\n")

pure_vnese_words_text_file.close()