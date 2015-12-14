"""
Означення власних "фільтрів", якими можна користатися в шаблонах
"""

import os
from django.template import Library
from koopsite.functions import get_user_full_name, \
                                get_user_flat_No
try:
    from PIL import Image
except ImportError:
    print('ImportError: from PIL import Image')
    import Image

register = Library()

@register.filter()
def get_at_index(list, index):
    # Фільтр для отримання елемента списку за його індексом
    try:    val = list[index]
    except: val = None
    return val

@register.filter()
def get_item_by_key(dictionary, key):
    # Фільтр для отримання значення словника за його ключем
    try:    val = dictionary.get(key)
    except: val = None
    return val

@register.filter()
def range_of(n):
    # Фільтр для отримання ітератора range(n) в шаблоні
    try:    val = range(n)
    except: val = None
    return val

# TODO-доробити тести для всіх наступних фільтрів

@register.filter()
def model_name(f):
    # Фільтр для назви моделі
    m = f._meta.model_name
    return m

@register.filter()
def user_full_name(user):
    # Фільтр для повного імені користувача
    fn = get_user_full_name(user)
    return fn

@register.filter()
def user_flat_No(user):
    # Фільтр для номера квартири з профілю користувача
    fn = get_user_flat_No(user)
    return fn

@register.filter()
def thumbnail(file, size='30x24'):
    """
    A filter to resize a ImageField on demand, a use case could be:
    <img src="{{ object.image.url }}" alt="original image">
    <img src="{{ object.image|thumbnail }}" alt="image resized to default 104x104 format">
    <img src="{{ object.image|thumbnail:200x300 }}" alt="image resized to 200x300">
    Original http://www.djangosnippets.org/snippets/955/
    :param file:    image url
    :param size:    size for thumbnail
    :return:        thumbnail url
    """
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filename = file.path
    filehead, filetail = os.path.split(filename)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    miniature_filename = os.path.join(filehead, miniature)
    fileurl = file.url
    filehead, filetail = os.path.split(fileurl)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and \
                                os.path.getmtime(filename) > \
                                os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        try:
            image = Image.open(filename)
            image.thumbnail([x, y], Image.ANTIALIAS)
            try:
                image.save(miniature_filename, image.format, quality=90, optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)
        except:
            pass
    return miniature_url

@register.filter()
def icon_yes_no_unknown(bool_val):
    """
    # Фільтр представлення поля NullBooleanField іконкою.
    """
    if   bool_val == True:  miniature_url = 'admin/img/icon-yes.gif'
    elif bool_val == False: miniature_url = 'admin/img/icon-no.gif'
    else:                   miniature_url = 'admin/img/icon-unknown.gif'
    return miniature_url

