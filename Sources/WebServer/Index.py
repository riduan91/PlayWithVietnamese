# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:27:42 2017

@author: ndoannguyen
"""

import cgi 

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

print(form.getvalue("name"))

html = """<!DOCTYPE html>
<head>
    <title>My program</title>
</head>
<body>
    <form action="/index.py" method="post">
        <input type="text" name="name" value="Your name" />
        <input type="submit" name="send" value="Send information to server">
    </form> 
</body>
</html>
"""

print(html)