# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 17:34:54 2017

@author: ndoannguyen
"""

import sys
sys.path.append("../Basic/")
sys.path.append("../Configuration/")
import configuration
from Word import Word

BASIC_DATA_DIR = configuration.BASIC_DATA_DIR
RAW_WORDS_FILE_NAME = configuration.RAW_WORDS_FILE_NAME
PURE_VNESE_SYLLABLES_FILE_NAME = configuration.PURE_VNESE_SYLLABLES_FILE_NAME

pure_vnese_syllable_collection = {}

for line in open(RAW_WORDS_FILE_NAME):
    line = line.replace("\n", "")
    word = Word(line)
    syllables = word.getSyllables()
    for syllable in syllables:
        syllable_text = syllable.getSyllable()
        if syllable.isPureVietnameseSyllable() and not pure_vnese_syllable_collection.has_key(syllable_text) :
            pure_vnese_syllable_collection[syllable_text] = 1

pure_vnese_syllables_text_file = open(PURE_VNESE_SYLLABLES_FILE_NAME, 'w')
for word in sorted(pure_vnese_syllable_collection.keys()):
    pure_vnese_syllables_text_file.write(word + "\n")

pure_vnese_syllables_text_file.close()