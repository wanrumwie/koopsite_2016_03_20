html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>Заголовок</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

import html.parser
import os
from bs4 import BeautifulSoup

startFolder = 'c:\pyPrograms\Django\koopsite'
html_file = 'koopsite/templates/base_koop.html'
html_file = os.path.join(startFolder, html_file)
with open(html_file, encoding='utf-8') as infile:
    html_doc = infile.read()
soup = BeautifulSoup(html_doc, 'html.parser')

print(html_doc)
print('-'*80)

print(soup.prettify())
print('-'*80)

for link in soup.find_all('a'):
    print(link.get('href'))

print('-'*80)

print(soup.get_text())
