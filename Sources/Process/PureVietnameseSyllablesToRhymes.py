# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:19:06 2017

@author: ndoannguyen
"""

BASIC_SOURCE_DIR = "../Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
import Constants
from Syllable import Syllable

BASIC_DATA_DIR = Constants.BASIC_DATA_DIR
PURE_VNESE_SYLLABLES_FILE_NAME = Constants.PURE_VNESE_SYLLABLES_FILE_NAME
RHYMES_FILE_NAME = Constants.RHYMES_FILE_NAME

rhymes = {}
for line in open(BASIC_DATA_DIR + PURE_VNESE_SYLLABLES_FILE_NAME):
    line = line.replace("\n", "")
    syllable = Syllable(line)
    rhyme = syllable.getRhyme().getRhyme()
    rhymes[rhyme] = 1

rhyme_file = open(BASIC_DATA_DIR + RHYMES_FILE_NAME, 'w')
for rhyme in sorted(rhymes.keys()):
    rhyme_file.write(rhyme + "\n")

rhyme_file.close()