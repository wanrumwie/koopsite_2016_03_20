'''
Означення власних "фільтрів", якими можна користатися в шаблонах
'''

import os
from django import template
from koopsite.functions import get_iconPathForFolder, \
                               get_iconPathByFileExt

register = template.Library()

@register.filter
def filename(f):
    # Фільтр для назви файла
    try:    n = os.path.basename(f.filename)
    except: n = ""
    return n

@register.filter
def fileext(f):
    # Фільтр для розширення файла
    try:    e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
    except: e = ""
    return e

@register.filter
def filetype(f):
    # Фільтр для типу файла (відповідно до розширення)
    try:    e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
    except: e = ""
    t = fileTypeByFileExt(e)
    return t

# Фільтр для назви файла-іконки (для моделей folder і report)
@register.filter
def iconpath(f):
    m = f._meta.model_name
    if m == 'folder':
        p = get_iconPathForFolder()
    elif m == 'report':
        try:    e = os.path.splitext(f.filename)[1]  # [0] returns path+filename
        except: e = ""
        p = get_iconPathByFileExt(e)
    else:
        p = ''
    return p
