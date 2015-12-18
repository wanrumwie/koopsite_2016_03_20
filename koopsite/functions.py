import os
import re
import json
from urllib.parse import unquote
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from math import ceil
from koopsite.fileExtIconPath import iconPath
from koopsite.settings import EMAIL_HOST_USER, TRACE_CONDITION

try:
    from PIL import Image, ImageOps
except ImportError:
    print('from PIL import Image, ImageOps: ImportError')
    import Image
    import ImageOps

def trace_print(*args):
    """
    Умовний друк, залежно від значення параметра TRACE_CONDITION з settings.py
    :param args:
    :return:
    """
    if TRACE_CONDITION:
        print(*args)

def print_list(list, name=''):
    print(name, 'len =', len(list))
    for i in list: print(i)

def print_dict(d, name=''):
    print(name, 'len =', len(d))
    for k,v in sorted(d.items()): print('%-20s : %s' % (k,v))

def round_up_division(a, b):
    """
    :param a: чисельник
    :param b: знаменник
    :return: частка, заокруглена до більшого цілого
    """
    r = ceil(float(a)/b)
    return r

def get_namespace_from_dict(d, ns, extend=False):
    """
    Функція, яка заповнює простір імен типу SimpleNameSpace
    даними звичайного словника.
    :param d: словник з даними
    :param ns: простір імен, який слід заповнити
    :param extend: при True простір імен доповнюється ключами з d
    :return: ns - заповнений даними словника простір імен,
            з яким можна оперувати у такий спосіб: ns.key замість d['key']
    """
    if extend:  # namespace will extend by dict fields
        keys = d.keys()
    else:       # namespace will not extend by dict fields
        keys = vars(ns).keys()
    for k in keys:
        vars(ns)[k] = d.get(k)
    return ns

def get_iconPathForFolder(openFlag=False):
    if openFlag: p = 'img/open_folder.png'
    else:        p = 'img/folder.png'
    # print('folder: p=', p)
    return p

def get_iconPathByFileExt(ext):
    p = iconPath.get(ext)
    if not p: p = "_page.png"
    directory = 'img/file-icons/32px/'
    p = directory + p
    # print('ext =', ext, '  p=', p)
    return p

def fileNameCheckInsert(fileName, fileNameList):
    '''
    Функція для визначення нового імені файла при його завантаженні
    Повне ім'я файла порівнюється із списком наявних імен.
    При співпадінні ім'я файла (перед розширенням) доповнюється
    номером копії у дужках, наприклад "qwerty (1).py"
    Якщо виявиться, що подібні назви вже існуть, буде знайдено
    найбільший номер копії, наприклад "qwerty (3).py"
    Функція повертає нову або стару назву файла
    а також доповнює змінюваний список файлів.
    '''
    if fileName in fileNameList:
        (name, ext) = os.path.splitext(fileName)
        pattern = '\((?P<xxx>\d+)\)'.join((re.escape(name+" "), re.escape(ext)))
        pattern = re.compile(pattern)
        i = 0
        for f in fileNameList:
            s = re.search(pattern, f)
            if s:
                j = int(s.group('xxx'))
                i = max(i,j)
        s = " (%s)" % (i+1)
        fileName = s.join((name, ext))
    fileNameList.append(fileName)
    return fileName

def sendMailToUser(user, subject="KoopSite administrator", message=""):
    email    = user.email
    send_mail(subject, message, EMAIL_HOST_USER, [email])
    # send_mail('Subject', 'Message.', 'from@example.com',
    #             ['john@example.com', 'jane@example.com'])

def scale_height(width, height, hmax):
    if height > hmax or hmax == 0:
        ratio = hmax*1./height if height != 0 else 0
        width = int(width*ratio)
        height = int(height*ratio)
    return (width, height)

def scale_width(width, height, wmax):
    if width > wmax or wmax == 0:
        ratio = wmax*1./width if width != 0 else 0
        width = int(width*ratio)
        height = int(height*ratio)
    return (width, height)


emptyElement = {'model'       : None,
                'id'          : None,
                'selRowIndex' : None,
                }

def getSelections(session):
    """
    Отримання даних про виділені елементи всіх таблиць з сесії.
    :param session: request.session
    :return: selections = {parent_id: selElement, ...}
    Формат даних в сесії:
    session = { ... ,
               'Selections':
                    {browTabName:
                         {parent_id:
                             {'model'       : model,
                              'id'          : id,
                              'selRowIndex' : selRowIndex,
                             },
                         },
                    },
               }
    де  browTabName: назва таблиці, напр. 'folders_contents', 'users_list'
        parent_id:  str(Folder.id) - ідентифікатор теки, яка відображається
        model: _meta.model_name - назва моделі виділеного елемента
        id: id виділеного елемента
        selRowIndex: порядковий номер виділеного елемента в таблиці
    """
    # Пробуємо отримати значення з сесії:
    selections = session.get('Selections')
    trace_print('getSelections: session =', session.items())
    # print('getSelections: selections =', selections)
    if (not selections) or (type(selections) != type({})):
        # якщо selections не існує або не є словником,
        # створюємо новий порожній словник:
        # browTabName   = ""
        # parent_id       = 0
        # tableSelections = {str(parent_id) : emptyElement}
        # selections      = {browTabName  : tableSelections}
        selections      = {}
        # print('getSelections: not: selections =', selections)
        # Записуємо в сесію:
        session['Selections'] = selections
    return selections

def getSelElementFromSession(session, browTabName, parent_id=''):
    """
    Отримання параметрів виділеного елемента таблиці folder_content
    з даних сесії.
    :param session: request.session
    :param browTabName: назва таблиці, у якій виділено елемент
    :param parent_id: ідентифікатор теки (якщо є),
                      яка відображається в таблиці
    :return selElement: словник з параметрами виділеного елемента
                { 'model'       : model,
                  'id'          : id,
                  'selRowIndex' : selRowIndex,
                } для теки з parent_id в таблиці browTabName
    """
    parent_id = str(parent_id)  # key in session must be str
    # Пробуємо отримати значення з сесії:
    selections = getSelections(session)
    tableSelections = selections.get(browTabName, {})
    selElement = tableSelections.get(parent_id, emptyElement)
    # print('getSelElementFromSession: selElement =', selElement)
    return selElement

def setSelElementToSession(session, browTabName, parent_id='',
                           selElement=emptyElement):
    """
    Запис в сесію параметрів виділеного елемента таблиці folder_content
    :param session: request.session
    :param browTabName: назва таблиці, у якій виділено елемент
    :param parent_id: ідентифікатор теки (якщо є),
                      яка відображається в таблиці
    :param selElement: словник з параметрами виділеного елемента
                { 'model'       : model,
                  'id'          : id,
                  'selRowIndex' : selRowIndex,
                } для теки з parent_id в таблиці browTabName
    """
    parent_id = str(parent_id)  # key in session must be str
    # Пробуємо отримати значення з сесії:
    selections = getSelections(session)
    tableSelections = selections.get(browTabName, {})
    # Встановлюємо нові значення:
    tableSelections[parent_id] = selElement
    selections[browTabName] = tableSelections
    # Записуємо в сесію:
    session['Selections'] = selections
    # print('setSelElementToSession:')
    # print('selElement =', selElement)

def parseClientRequest(request):
    """
    Розбираємо запит від клієнта
    :param request:
    :return  d: одновимірний словник
    Формат запиту від клієнта:
    {'client_request' : json_s}
    json_s --> розкодування --> d - словник з даними про материнську
                                    теку і виділений елемент
    Формат d: { 'browTabName'   : browTabName,
                'parent_id'     : parent_id,
                'model'         : model,
                'id'            : id,
                'selRowIndex'   : selRowIndex,
                'name'          : name,
               }
    Кожна ф-ція ajax...view (.py) витягне з цього словника необхідні дані,
    в тому числі і якщо ajax... (.js) пошле додатковий елемент,
    що не входить до "стандартного" набору keys.
    """
    # Отримуємо запит з даними від клієнта:
    json_s = request.POST['client_request']
    # Розкодовуємо стрічку JSON в звичайний словник
    d = json.loads(json_s)
    # Стандартний набір ключів:
    keys = ['browTabName',
            'parent_id'  ,
            'model'      ,
            'id'         ,
            'selRowIndex',
            'name'       ,
            'sendMail'   ,
            ]
    # Перевіряємо наявність ключів і заповнюємо відсутні значенням None
    for key in keys:
        if not key in d.keys():
            d[key] = None
    # print('parseClientRequest: d=', d)
    return d

def parseXHRClientRequest(request):
    """
    Розбираємо xhr запит від клієнта
    :param request:
    :return:  d - словник з даними про материнську теку і інш.
    Формат запиту від клієнта:
    encoded_json_string знаходиться у заголовку "X-client-request"
    Кожна ф-ція xhr ajax...view витягне з словника d необхідні дані
    """
    # Отримуємо запит з даними від клієнта:
    encoded_json_s = request.META.get("HTTP_X_CLIENT_REQUEST")
    # Розкодовуємо в UTF8:
    json_s = unquote(encoded_json_s)
    # Розкодовуємо стрічку JSON в звичайний словник
    d = json.loads(json_s)
    # print('parseXHRClientRequest: d=', d)
    return d


def get_user_full_name(user):
    fn = (x.strip().capitalize() for x in (user.last_name, user.first_name))
    s = ' '.join(fn)
    return s.strip()

def get_user_flat_No(user):
    try:
        s = user.userprofile.flat.flat_No
    except:
        s = ""
    return s

def get_user_is_recognized(user):
    try:
        s = user.userprofile.is_recognized
    except:
        s = ""
    return s

def print_user_permissions(user):
    print('='*50)
    print('user:', user)
    print('-'*50)
    print('get_all_permissions:')
    user_permissions = user.get_all_permissions()
    for p in sorted(user_permissions):
        print(p)
    print('-'*50)
    print('groups:')
    for g in user.groups.all():
        print(g.name)
    print('-'*50)

def is_staff_only(user):
    groups = user.groups.all()
    staff  = Group.objects.get(name='staff')
    return staff in groups and len(groups) == 1

def has_group_member(user):
    return has_group(user, 'members')

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def add_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.add(group)

def remove_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.remove(group)


class AllFieldsMixin():
    """
    Базовий клас, який робить вибірку ВСІХ полів будь-якого одного
    запису або всіх записів моделі. Методи класу формують дані
    у вигляді списків, зручних до використання в шаблонах.
    Підмішуючи цей клас до CBV і переозначуючи там лише
    get_context_data() можна отримати клас-представлення для всіх
    полів одного запису або всіх полів всіх записів обраної моделі.
    """
    model   = None  # модель слід зазначити у дочірньому класі
    fields  = ()    # Поля, які будуть виведені. Якщо порожній, то всі.
    exclude = ()    # Поля, які виключаються із списку виводу.

    def val_repr(self, v, decimal=2):
        """
        Представлення значення у шаблоні.
        Заокруглює число. Для нуля повертає "".
        У дочірньому класі можна переозначити для специфічних потреб,
        наприклад, щоб floor_No = 0 ДРУКУВАЛОСЬ ЯК 0, а не ""
        """
        # TODO-floor_No = 0 виводиться як "" - виправити!
        try:    v = round(v, decimal)
        except: pass
        if v == 0: v = ""
        return v

    def get_field_keys_verbnames(self):
        """
        Визначення списку пар: (name, verbose_name) для кожного
          поля моделі self.model. Маючи цей перелік легко отримати
          список значень всіх полів для будь-якого-запису моделі.
        :return keys: список ідентифікаторів полів моделі за мінусом excluded
        :return verb: список людських найменувань полів моделі за мінусом excluded
        """
        keys = []
        verb = []
        if self.fields:
            for k in self.fields:
                if k not in self.exclude:
                    fo = self.model._meta.get_field(k)
                    vn = fo.verbose_name
                    keys.append(k)
                    verb.append(vn)
        else:
            for fo in self.model._meta.fields:
                k = fo.name
                vn = fo.verbose_name
                if k not in self.exclude:
                    keys.append(k)
                    verb.append(vn)
        return keys, verb

    def get_value_list(self, record, keys):
        """
        Отримання списку значень полів
        :param record: об'єкт моделі
        :param keys: список полів, синхронно якому створиться список значень
        :return: values - список значень
        """
        values = []
        for k in keys:
            v = getattr(record, k)
            v = self.val_repr(v, 2)
            values.append(v)
        return values

    def get_label_value_list(self, keys, values):
        """
        Отримання списку, що складається з кортежів (key, value)
        :param keys: список ідентифікаторів полів моделі
        :param values: список значень полів моделі
        :return: [(k, v), ...]
        """
        return [(k, v) for k, v in zip(keys, values)]

