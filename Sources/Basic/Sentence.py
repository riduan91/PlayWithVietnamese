# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:57:14 2017

@author: ndoannguyen
"""

import sys
sys.path.append("../Import")

from Syllable import Syllable
from Word import Word
import re
import LoadPureVietnameseWords

PURE_VNESE_WORDS = LoadPureVietnameseWords.PURE_VNESE_WORDS

class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence.replace(".", "").replace(",", "")
        self.syllables = [Syllable(syllable) for syllable in re.split('[ ]+', self.sentence)]
        self.length = len(self.syllables)
        self.splitSentenceToWords()
    
    def getSentence(self):
        return self.sentence
    
    def getSyllables(self):
        return self.syllables
    
    def getWords(self):
        return self.words
        
    def splitSentenceToWordsFromLeft(self):
        sentence_length = self.length
        syllables = [self.syllables[i].getSyllable() for i in range(sentence_length)]
        current_position = 0
        words = []
        while (current_position != sentence_length):
            for i in range (min(4, sentence_length - current_position), 0, -1):
                possible_word = " ".join(syllables[current_position : current_position + i])
                if possible_word.decode('utf-8') in PURE_VNESE_WORDS:
                    words.append(Word(possible_word))
                    current_position += i
                    break
                if i==1:
                    words.append(Word(possible_word))
                    current_position += 1
        self.words = words
        
    def splitSentenceToWords(self):
        self.splitSentenceToWordsFromLeft()