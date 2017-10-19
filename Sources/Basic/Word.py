# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:17:36 2017

@author: ndoannguyen
"""

import re
from Syllable import Syllable

class Word:
    def __init__(self, word):
        self.word = word
        self.splitWordToSyllables()
        self.checkPureVietnameseWord()
    
    def splitWordToSyllables(self):
        self.raw_syllables = re.split('[ ]+', self.word)
        self.syllables = [Syllable(syllable) for syllable in self.raw_syllables]
    
    def checkPureVietnameseWord(self):
        self.pure_Vietnamese = True
        for syllable in self.syllables:
            if not syllable.isPureVietnameseSyllable():
                self.pure_Vietnamese = False
                break
    
    def getWord(self):
        return self.word
    
    def getSyllables(self):
        return self.syllables
    
    def getRhyme(self):
        return self.syllables[-1].getRhyme()
    
    def getAccent(self):
        return self.syllables[-1].getAccent()
    
    def getLength(self):
        return len(self.syllables)
    
    def isPureVietnameseWord(self):
        return self.pure_Vietnamese