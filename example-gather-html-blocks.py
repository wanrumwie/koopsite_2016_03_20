import html.parser
import os
from bs4 import BeautifulSoup

# base_dir = 'c:\pyPrograms\Django\koopsite'
# html_file = 'koopsite/templates/koop_base.html'
# html_file = os.path.join(base_dir, html_file)
# with open(html_file, encoding='utf-8') as infile:
#     html_doc = infile.read()

html_doc = '''
<Text Node: '﻿<!DOCTYPE html>

'>
<Text Node: '

<html xmlns="http://www'>
<Block Node: load_style. Contents: [<Text Node: '
        '>, <django.template.defaulttags.LoadNode object at 0x04B3B8B0>, <Text Node: '
        <link rel="style'>, <django.contrib.staticfiles.templatetags.staticfiles.StaticFilesNode object at 0x04B3B890>, <Text Node: '" />
        <link rel="i'>, <django.contrib.staticfiles.templatetags.staticfiles.StaticFilesNode object at 0x04B3B8D0>, <Text Node: '"/>
        <link rel="sh'>, <django.contrib.staticfiles.templatetags.staticfiles.StaticFilesNode object at 0x04B3B8F0>, <Text Node: '"/>
    '>]>
<Text Node: '

    '>
<Block Node: style. Contents: [<Text Node: '
        '>, <Text Node: '
    '>]>
<Text Node: '

</head>

<body>
 <div c'>
<Block Node: title. Contents: [<Text Node: '
        '>, <django.template.loader_tags.IncludeNode object at 0x04B3B910>, <Text Node: '
    '>]>
<Text Node: '
  </div>

  <div class="'>
<Text Node: '
        '>
<Block Node: href-index. Contents: [<Text Node: '
            <li><a href='>, <django.template.defaulttags.URLNode object at 0x04B2D6B0>, <Text Node: '">Головна сторінка</a></l'>]>
<Text Node: '
        '>
<Block Node: href-flats. Contents: [<Text Node: '
            <li><a href='>, <django.template.defaulttags.URLNode object at 0x04B2D8F0>, <Text Node: '">Квартири</a></li>
     '>]>
<Text Node: '
        '>
<Block Node: href-folders. Contents: [<Text Node: '
            <li><a href='>, <django.template.defaulttags.URLNode object at 0x04B2D9B0>, <Text Node: '">Документи</a></li>
    '>]>
<Text Node: '
        '>
<Block Node: href-login. Contents: [<Text Node: '
            '>, <IfNode>, <Text Node: '
        '>]>
<Text Node: '
        '>
<Block Node: href-register. Contents: [<Text Node: '
            '>, <IfNode>, <Text Node: '
        '>]>
<Text Node: '
        '>
<Block Node: href-own-profile. Contents: [<Text Node: '
            '>, <IfNode>, <Text Node: '
        '>]>
<Text Node: '
        '>
<Block Node: href-adm-index. Contents: [<Text Node: '
            '>, <IfNode>, <Text Node: '
        '>]>
<Text Node: '
        '>
<Block Node: href-back. Contents: [<Text Node: '
            <li><a href='>]>
<Text Node: '
    </ul>

    '>
<Block Node: body. Contents: [<Text Node: '
        '>, <Text Node: '
    '>]>
<Text Node: '

    '>
<Block Node: paginator. Contents: [<Text Node: '
        '>, <Text Node: '
        '>, <Text Node: '
        '>, <django.template.loader_tags.IncludeNode object at 0x04B3B210>, <Text Node: '
    '>]>
<Text Node: '

  </div>

  <div class='>
<Block Node: bottom. Contents: [<Text Node: '
        '>, <django.template.loader_tags.IncludeNode object at 0x04B3B290>, <Text Node: '
    '>]>
<Text Node: '
  </div>
 </div>
</body>'>
<django.template.defaulttags.CommentNode object at 0x04B15E50>
<Text Node: '
'>
'''

soup = BeautifulSoup(html_doc, 'html.parser')

print(html_doc)
print('-'*80)

print(soup.prettify())
print('-'*80)

for link in soup.find_all('a'):
    print(link.get('href'))

print('-'*80)

print(soup.get_text())
