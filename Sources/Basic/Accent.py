# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:01:43 2017

@author: ndoannguyen
"""

def areCompatibleAccents(accent1, accent2):
    """
        Kiểm tra hai thanh điệu cùng bằng hoặc cùng trắc, trả lại True nếu cùng loại và False nếu khác loại hoặc vô định
    """
    type1 = 0
    type2 = 0
    if accent1 in "zf":
        type1 = 1
    elif accent1 in "srxj":
        type1 = 2
    if accent2 in "zf":
        type2 = 1
    elif accent2 in "srxj":
        type2 = 2
    return (type1 != 0 and type2 != 0 and type1 == type2)