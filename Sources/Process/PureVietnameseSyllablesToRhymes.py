# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:19:06 2017

@author: ndoannguyen
"""

import sys
sys.path.append("../Basic/")
sys.path.append("../Configuration/")
import configuration
from Syllable import Syllable

BASIC_DATA_DIR = configuration.BASIC_DATA_DIR
PURE_VNESE_SYLLABLES_FILE_NAME = configuration.PURE_VNESE_SYLLABLES_FILE_NAME
RHYMES_FILE_NAME = configuration.RHYMES_FILE_NAME

rhymes = {}
for line in open(PURE_VNESE_SYLLABLES_FILE_NAME):
    line = line.replace("\n", "")
    syllable = Syllable(line)
    rhyme = syllable.getRhyme().getRhyme()
    rhymes[rhyme] = 1

rhyme_file = open(RHYMES_FILE_NAME, 'w')
for rhyme in sorted(rhymes.keys()):
    rhyme_file.write(rhyme + "\n")

rhyme_file.close()