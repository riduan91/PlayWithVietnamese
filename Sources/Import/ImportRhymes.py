# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:59:17 2017

@author: ndoannguyen
"""

import sys
sys.path.append("../Basic")
sys.path.append("../Configuration")
from Rhyme import Rhyme
import configuration

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
RhymeCollection = VietnameseDB['Rhymes']

RHYMES_FILE_NAME = configuration.RHYMES_FILE_NAME

all_rhymes = []

reader = open(RHYMES_FILE_NAME)
for line in reader:
    line = line.replace("\n", "").replace("\r", "").split("-")
    rhyme = Rhyme(line[0], line[1], line[2])
    all_rhymes.append(rhyme)

index = 1

for rhyme in all_rhymes:
    quasi_rhymable_rhymes = []
    for another_rhyme in all_rhymes:
        if rhyme.isQuasiRhymable(another_rhyme):
            quasi_rhymable_rhymes.append(another_rhyme.getRhyme())
    rhyme_mongo_document = {
                        "_id": "RHY" + str(index).zfill(5),
                        "rhyme" : rhyme.getRhyme(),
                        "secondary_part" : rhyme.getSecondaryPart(),
                        "primary_part" : rhyme.getPrimaryPart(),
                        "end_part" : rhyme.getEndPart(),
                        "quasi_rhymable_rhymes" : quasi_rhymable_rhymes
                    }
    try:
        RhymeCollection.insert_one(rhyme_mongo_document)
        index += 1
    except DuplicateKeyError:
        print "[Error] Rhyme with id %s already exists." % ("RHY" + str(index).zfill(5))
        index += 1