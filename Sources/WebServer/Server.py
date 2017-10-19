#!/usr/bin/env python
# -*- coding:utf-8 -*-

import operator
from flask import Flask, render_template, request
app = Flask(__name__)

BASIC_SOURCE_DIR = "../Basic/"
MONGO_SOURCE_DIR = "../Mongo/"
import sys
sys.path.append(BASIC_SOURCE_DIR)
sys.path.append(MONGO_SOURCE_DIR)

from FindQuasiRhymableWords import findQuasiRhymableWords 
from Word import Word

@app.route("/")
def app1():
   return render_template("app1.html")
   
@app.route('/find_rhymable_words', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        parameters = request.form
        rhymable_words_cursor = findQuasiRhymableWords(Word(parameters['myword'].encode('utf-8')), 'WordsInTruyenKieu', int(parameters['mylimit']))
        rhymable_words = {}
        try:
            for another_word in rhymable_words_cursor:
                rhymable_words[another_word['word']] = another_word['popularity']
        except TypeError:
            pass
        rhymable_words = sorted(rhymable_words.iteritems(), key=operator.itemgetter(1), reverse=True)
        return render_template("result.html", result = (parameters, rhymable_words))
    else:
        return render_template("app1.html")
    
port = 8800
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8800, debug=True)