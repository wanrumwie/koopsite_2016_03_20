import json
import os
import re
import string
from urllib.parse import unquote
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from math import ceil
from koopsite.fileExtIconPath import iconPath
from koopsite.settings import EMAIL_HOST_USER, TRACE_CONDITION


def trace_print(*args):
    """
    Умовний друк, залежно від значення параметра TRACE_CONDITION з settings.py
    :param args:
    :return:
    """
    if TRACE_CONDITION:
        print(*args)

def list_print(list, name=''):
    print(name, 'len =', len(list))
    for i in list: print(i)

def dict_print(d, name=''):
    try:    length = len(d)
    except: length = len(d.__dict__)
    print(name, 'len =', length)
    try:
        for k, v in sorted(d.items()): print('%-20s : %s' % (k, v))
    except:
        for k, v in sorted(d.__dict__.items()): print('%-20s : %s' % (k, v))


def user_permissions_print(user):
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


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def round_up_division(a, b):
    """
    :param a: чисельник
    :param b: знаменник
    :return: частка, заокруглена до більшого цілого
    """
    r = ceil(float(a)/b)
    return r

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

def parseClientRequest(requestPOST):
    """
    Розбираємо запит від клієнта
    :param requestPOST: request.POST
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
    json_s = requestPOST['client_request']
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
    # print('json_s =', json_s)
    # print('parseClientRequest: d=', d)
    return d

def parseXHRClientRequest(requestMETA):
    """
    Розбираємо xhr запит від клієнта
    :param requestMETA: request.META
    :return:  d - словник з даними про материнську теку і інш.
    Формат запиту від клієнта:
    encoded_json_string знаходиться у заголовку "X-client-request"
    Кожна ф-ція xhr ajax...view витягне з словника d необхідні дані
    """
    # Отримуємо запит з даними від клієнта:
    encoded_json_s = requestMETA.get("HTTP_X_CLIENT_REQUEST")
    # Розкодовуємо в UTF8:
    json_s = unquote(encoded_json_s)
    # Розкодовуємо стрічку JSON в звичайний словник
    d = json.loads(json_s)
    # print('requestMETA =', requestMETA)
    # print('encoded_json_s =', encoded_json_s)
    # print('json_s =', json_s)
    # print('parseXHRClientRequest: d=', d)
    return d

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

def is_staff_only(user):
    groups = user.groups.all()
    staff  = get_or_none(Group, name='staff')
    return staff in groups and len(groups) == 1

def has_group_member(user):
    return has_group(user, 'members')

def has_group(user, group_name):
    group = get_or_none(Group, name=group_name)
    return group in user.groups.all()

def add_group(user, group_name):
    group = get_or_none(Group, name=group_name)
    user.groups.add(group)

def remove_group(user, group_name):
    group = get_or_none(Group, name=group_name)
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


def transliterate(s, lang_from='uk', lang_to='en'):
    """
    Функція транслітерації. За промовчанням призначена для
    запису українських літер латинськими за правилами,
    встановленими постановою КМУ від 2010р.
    :param s: вхідна стрічка
    :param lang_from: мова вхідної стрічки
    :param lang_to: мова вихідної стрічки
    :return: транслітерована стрічка
    Параметри мов вставлені на перспективу. Потрібно буде змінити
    значення map, diphthong_map та word_start_map.
    Неукраїнські літери і символи, які не входять до складу
    списку string.printable будуть замінені на символ підкреслення '_'.
    """
    # Загальні правила заміни літер:
    map = {
            'А': 'A',
            'Б': 'B',
            'В': 'V',
            'Г': 'H',
            'Д': 'D',
            'Е': 'E',
            'Ж': 'Zh',
            'З': 'Z',
            'И': 'Y',
            'Й': 'I',
            'К': 'K',
            'Л': 'L',
            'М': 'M',
            'Н': 'N',
            'О': 'O',
            'П': 'P',
            'Р': 'R',
            'С': 'S',
            'Т': 'T',
            'У': 'U',
            'Ф': 'F',
            'Х': 'Kh',
            'Ц': 'Ts',
            'Ч': 'Ch',
            'Ш': 'Sh',
            'Щ': 'Shch',
            'Ь': '',
            'Ю': 'Iu',
            'Я': 'Ia',
            'Є': 'Ie',
            'І': 'I',
            'Ї': 'I',
            'Ґ': 'G',
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'h',
            'д': 'd',
            'е': 'e',
            'ж': 'zh',
            'з': 'z',
            'и': 'y',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'ts',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ь': '',
            'ю': 'iu',
            'я': 'ia',
            'є': 'ie',
            'і': 'i',
            'ї': 'i',
            'ґ': 'g',
    }
    # Правила заміни літер на початку слова:
    word_start_map = {
            'Й': 'Y',
            'Ю': 'Yu',
            'Я': 'Ya',
            'Є': 'Ye',
            'Ї': 'Yi',
            'й': 'y',
            'ю': 'yu',
            'я': 'ya',
            'є': 'ye',
            'ї': 'yi',
    }
    # Правила заміни дифтонгів (в українській мові для цілей
    # транслітерації під дифтонгом розуміється лише буквосполучення 'зг'.
    diphthong_map = {
            'ЗГ': 'ZGh',
            'Зг': 'Zgh',
            'зг': 'zgh',
    }
    if lang_from == 'uk' and lang_to == 'en':
        # Спочатку обробка дифтонгів:
        for a in diphthong_map:
            s = s.replace(a, diphthong_map[a])

        # Обробка початків слів:
        words = s.split()
        for i in range(len(words)):
            word = words[i]
            for a in word_start_map:
                if word.startswith(a):
                    b = word_start_map[a]
                    word = word.replace(a, b, 1)
                    words[i] = word
                    break
        s = ' '.join(words)

        # Обробка основної маси літер:
        trans = []
        for a in s:
            if a in map:
                b = map[a]
            elif not a in string.printable:
                b = '_'
            else:
                b = a
            trans.append(b)
        s = ''.join(trans)
    return s

#---------------- Кінець коду, охопленого тестуванням ------------------


def sendMailToUser(user, subject="KoopSite administrator", message=""):
    email    = user.email
    send_mail(subject, message, EMAIL_HOST_USER, [email])
    # send_mail('Subject', 'Message.', 'from@example.com',
    #             ['john@example.com', 'jane@example.com'])


