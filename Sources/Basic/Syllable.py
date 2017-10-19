# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:08:18 2017
@author: ndoannguyen
"""

import Constants
from VLetter import ToLowerVLetter
from Accent import areCompatibleAccents
from Rhyme import Rhyme

class Syllable:
    
    def __init__(self, syllable):
        self.syllable = syllable
        self.SplitSyllableToParts()
        self.checkPureVietnameseSyllable()
    
    def SplitSyllableToParts(self):
        """
            Tách một tiếng thành 3 phần: phụ âm đầu, vần và thanh
            Kí hiệu thanh: Ngang: z, Huyền: f, Sắc: s , Hỏi: r, Ngã: x, Nặng: j
        """
        self.SplitSyllableToVLetters()
        composed_vletters = self.composed_vletters
        nb_vletters = len(composed_vletters)
        beginning_consonant = ""
        rhyme = ""
        accent = "z"
        consonant_terminated = 0
        for i in range(nb_vletters):
            if composed_vletters[i] in Constants.LOWER_CONSONANT_VLETTER_LIST and consonant_terminated == 0:
                beginning_consonant += composed_vletters[i]
            elif composed_vletters[i] in Constants.REMOVE_ACCENT_FROM_VLETTER:
                rhyme += Constants.REMOVE_ACCENT_FROM_VLETTER[composed_vletters[i]]
                accent = Constants.TAKE_ACCENT_FROM_VLETTER[composed_vletters[i]]
                consonant_terminated = 1
            else:
                rhyme += composed_vletters[i]
                consonant_terminated = 1
    
        if beginning_consonant == "g" and rhyme.startswith("i"):
            beginning_consonant = "gi"
            for i in range(min(2, len(rhyme) - 1), 0, -1):
                if (rhyme[1 : 1 + i] in Constants.GI_INCOMPATIBLE):
                    rhyme = rhyme[1:]
                    break
    
        self.beginning_consonant = beginning_consonant
        self.raw_rhyme = rhyme
        self.accent = accent
        self.SplitRhymeToSmallParts()
        
        beginning_consonant = beginning_consonant.replace("k", "c").replace("q", "c").replace("gh", "g").replace("ngh", "ng")
      
    
    def SplitSyllableToVLetters(self):
        """
            Tách một tiếng thành các chữ cái (chữ cái = chữ cái đội dấu thanh), giữ nguyên trạng thái viết hoa
            Ví dụ: "Tiễn -> [T, i, ễ, n]"
        """
        syllable = self.syllable
        syllable_length = len(syllable)
        current_position = 0
        composed_vletters = []
        while (current_position != syllable_length):
            for i in range (min(3, syllable_length - current_position), 0, -1):
                if (syllable[current_position : current_position + i] in Constants.VLETTER_LIST):
                    composed_vletters.append(ToLowerVLetter(syllable[current_position : current_position + i]))
                    current_position += i
                    break
                if i==1:
                    composed_vletters.append(ToLowerVLetter(syllable[current_position]))
                    current_position += 1
        self.composed_vletters = composed_vletters 
        self.syllable = "".join(composed_vletters)
        
    def SplitRhymeToSmallParts(self):
        """
            Tách vần thành âm đệm (secondary_part), âm chính (primary_part), âm cuối (end_part)
        """
        rhyme = self.raw_rhyme
        secondary_part = ""
        primary_part = ""
        end_part = ""
        # Xử lí âm đệm: âm đệm chỉ có thể là o hoặc u và đứng trước các nguyên âm như dưới đây
        if rhyme.startswith("oa") or rhyme.startswith("oe") or (rhyme.startswith("ua") and self.beginning_consonant =='q') or rhyme.startswith("ue") \
            or rhyme.startswith("oă") or rhyme.startswith("uă") or rhyme.startswith("uâ")\
            or rhyme.startswith("uê") or rhyme.startswith("uy") or rhyme.startswith("uơ"):
                rhyme = rhyme[1:]
                secondary_part = "u"
        # Trường hợp âm cuối là phụ âm
        if rhyme.endswith("n") or rhyme.endswith("t") or rhyme.endswith("m") or rhyme.endswith("p") or rhyme.endswith("c"):
            end_part = rhyme[-1]
            primary_part = rhyme[:-1]
        elif rhyme.endswith("ng") or rhyme.endswith("nh") or rhyme.endswith("ch"):
            end_part = rhyme[-2:]
            primary_part = rhyme[:-2]
        # Trường hợp âm cuối là bán âm
        elif (rhyme.endswith("o") and rhyme != "o") or (rhyme.endswith("u") and rhyme != "u"):
            end_part = "u"
            primary_part = rhyme[:-1]
            # Chú ý: au thật ra là ă + bán âm cuối u
            if (rhyme == "au"):
                primary_part = "ă"
        elif (rhyme.endswith("i") and rhyme != "i") or (rhyme.endswith("y") and rhyme != "y"):
            end_part = "i"
            primary_part = rhyme[:-1]
            # Chú ý: ay thật ra là ă + bán âm cuối i
            if (rhyme == "ay"):
                primary_part = "ă"
        else:
            primary_part = rhyme
    
        # Xử lí nguyên âm đôi: đưa ia về iê trong trường hợp không có âm cuối; tương tự với ua -> uô, ưa -> ươ, thống nhất cách viết y thành i
        primary_part = primary_part.replace("y", "i").replace("ia", "iê").replace("ua", "uô").replace("ưa", "ươ")
        self.rhyme = Rhyme(secondary_part, primary_part, end_part)
        
    def checkPureVietnameseSyllable(self):
        self.pure_Vietnamese = True
        if self.beginning_consonant != "" and self.beginning_consonant not in Constants.V_PURE_CONSONANTS:
            self.pure_Vietnamese = False
        else:
            rhyme = self.rhyme
            if rhyme.secondary_part != "" and rhyme.secondary_part not in Constants.V_PURE_SECONDARY_PARTS:
                self.pure_Vietnamese = False
            elif rhyme.primary_part not in Constants.V_PURE_PRIMARY_PARTS:
                self.pure_Vietnamese = False
            elif rhyme.end_part != "" and rhyme.end_part not in Constants.V_PURE_END_PARTS:
                self.pure_Vietnamese = False
            elif self.accent not in Constants.V_PURE_ACCENTS:
                self.pure_Vietnamese = False
            elif rhyme.end_part in ["c", "t", "p", "ch"] and self.accent in ["z", "f", "r", "x"]:
                self.pure_Vietnamese = False
    
    def getSyllable(self):
        return self.syllable
    
    def setSyllable(self, syllable):
        self.syllable = syllable
        self.SplitSyllableToParts()
        
    def getComposedVLetters(self):
        return self.composed_vletters
        
    def getBeginningConsonant(self):
        return self.beginning_consonant
    
    def getRhyme(self):
        return self.rhyme
    
    def getAccent(self):
        return self.accent
    
    def getLength(self):
        return len(self.composed_vletters)
    
    def getTechnicalLength(self):
        return len(self.syllable)
    
    def isPureVietnameseSyllable(self):
        return self.pure_Vietnamese
    
    def isRhymable(self, AnotherSyllable):
        """
            Kiểm tra hai tiếng vần tuyệt đối với nhau, trả lại 
            0 nếu không hề vần
            1 nếu vần tuyệt đối
            2 nếu vần chỉ sai khác âm đệm
            3 nếu vần theo phương ngữ Nam
        """
        rhyme1, accent1 = self.getRhyme(), self.getAccent()
        rhyme2, accent2 = AnotherSyllable.getRhyme(), AnotherSyllable.getAccent()
        if rhyme1.isTotallyRhymable(rhyme2) and areCompatibleAccents(accent1, accent2):
            return 1
        elif rhyme1.isRhymableWithoutSecondaryPart(rhyme2) and areCompatibleAccents(accent1, accent2):
            return 2
        elif rhyme1.isQuasiRhymable(rhyme2) and areCompatibleAccents(accent1, accent2):
            return 3
        return 0