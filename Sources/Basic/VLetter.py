# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:52:52 2017

@author: ndoannguyen
"""

import Constants

def ToLowerVLetter(vletter):
    """
        Chuyển chữ cái thành in thường
    """
    if vletter in Constants.CONSONANT_VLETTER_DICTIONARY:
        return Constants.CONSONANT_VLETTER_DICTIONARY[vletter]
    elif vletter in Constants.VOWEL_VLETTER_DICTIONARY:
        return Constants.VOWEL_VLETTER_DICTIONARY[vletter]
    else:
        return vletter