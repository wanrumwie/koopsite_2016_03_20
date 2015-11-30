import json
import types
from django.http.response import HttpResponse
from django.shortcuts import render
from koopsite.functions import  getSelElementFromSession, \
                        setSelElementToSession, \
                        parseClientRequest

# Константа для типів повідомлення,
# яке сервер посилає клієнту через AJAX:
msgType = types.SimpleNamespace(
                Change        = "Change",
                DeleteRow     = "DeleteRow",
                Error         = "Error",
                Forbidden     = "Forbidden",
                IncorrectData = "IncorrectData",
                MoveElement   = "MoveElement",
                NewRow        = "NewRow",
                NoChange      = "NoChange",
                Normal        = "Normal",
                Rename        = "Rename",
                Group         = "Group",
                )

#################################################################
# jQuery ajax functions:
#################################################################

def ajaxSelRowIndexToSession(request):
    if 'client_request' in request.POST:
        # Розбираємо дані від клієнта:
        d = parseClientRequest(request)
        browTabName = d['browTabName']
        parent_id   = d['parent_id']
        # Формуємо дані для зберігання в сесії:
        selElement = {}
        selElement['model'      ] = d['model'      ]
        selElement['id'         ] = d['id'         ]
        selElement['selRowIndex'] = d['selRowIndex']
        # Записуємо в сесію:
        setSelElementToSession(request.session,
                                            browTabName=browTabName,
                                            parent_id=parent_id,
                                            selElement=selElement)
        # Посилаємо відповідь клієнту:
        response_dict = {'server_response': selElement }
        # return JsonResponse(response_dict)
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        return render(request, 'folders/folder_contents.html')

def ajaxStartRowIndexFromSession(request):
    if 'client_request' in request.POST:
        # Розбираємо дані від клієнта:
        d = parseClientRequest(request)
        browTabName = d['browTabName']
        parent_id   = d['parent_id']
        # Беремо з сесії масив параметрів виділеного елемента
        # для даної таблиці і для даного parent_id (якщо є):
        selElement = getSelElementFromSession(request.session,
                                            browTabName=browTabName,
                                            parent_id=parent_id)
        # Посилаємо відповідь клієнту:
        response_dict = {'server_response': selElement }
        # return JsonResponse(response_dict)
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        return render(request, 'folders/folder_contents.html')


#################################################################
# Базовий клас для формування 2D таблиці, яка поступає в шаблон
# одночасно з синхронним рендерингом, і дозволяє оперативно
# змінювати дані з допомогою jQuery ajax:
# Виклик:
# bta = BrowseTableArray()
# qs_array, sel_index = bta.get_qs_array(qs, sel_model_id)
# qs_array            = bta.get_qs_array(qs)
# headers = bta.get_table_headers()
#################################################################

class BrowseTableArray():
    columnsNumber   = 8        # number of columns in table

    def get_qs_array(self, qs, sel_model_id = None):
        """
        Визначає двомірний масив даних таблиці.
        Цей масив передається в шаблон синхронно при відкритті таблиці.
        Масив зберігається в невидимому полі шаблону
        і використовується для сортування таблиці
        (а також перейменування, додавання, видалення елементів)
        без перезавантаження сторінки.
        Формат масиву:
         arr[i][j] ,
         де i - номер рядка в таблиці (поч. з 0)
            j - номер колонки в таблиці (поч. з 1)
            arr[i][0] - словник з даними про примірник:
                        {'id': u.id, 'model': m, 'name': name}
        :param qs: queryset - послідовність примірників user
        :param sel_model_id: {'id': f.id, 'model': m} параметри вибраного рядка
        :return arr: 2D-масив значень таблиці + службова 0-ва колонка
        :return sel_index: порядковий номер вибраного рядка
        """
        # Власне таблиця (з службовою колонкою j=0)
        arr = {}
        if sel_model_id:        # є параметри пошуку => треба шукати
            need_search = True
        else:                   # вибириємо 0 => шукати не треба
            need_search = False
        sel_index = 0           # зміниться, якщо буде знайдено
        i = 0
        for u in qs:
            row = self.get_row(u)
            arr[i] = row
            if need_search:
                if (sel_model_id['id'   ] == row[0]['id'   ]) and \
                   (sel_model_id['model'] == row[0]['model']):
                    sel_index = i           # знайдено
                    need_search = False
            i += 1
        if sel_model_id != None:        # були параметри пошуку
            return arr, sel_index
        else:                   # параметрів пошуку не було
            return arr

    def get_table_headers(self):
        # Цей метод потрібно переозначити в дочірньому класі
        # Шапка таблиці для кожної колонки, починаючи з 1.
        # Нульова колонка - службова
        cap = {}
        cap[0] = ""
        cap[1] = "Name"
        return cap

    # Всі наступні методи можуть працювати незалежно від створення
    # таблиці qs_array і дозволяють працювати з окремими примірниками
    # класів (напр. Users, Folder, Report)
    # Виклик (наприклад):
    # changes = BrowseTableArray.get_cell_changes(old, new):

    def get_row(self, u):
        # Цей метод потрібно переозначити в дочірньому класі
        """
        Визначає один рядок у двомірному масиві даних таблиці.
        Формат рядка:
         row - словник {j: val},
         де j - номер колонки в таблиці (поч. з 1)
            val - значення j-ї клітинки
         Службове поле:
            row[0] - словник з даними про примірник:
                        {'id': u.id, 'model': m, 'name': name}
        :param u: примірник user
        :return row: одновимірний словник
        """
        if u:
            row = {}
            row[0] = self.get_model_id_name(u)
        else: # елемента нема => рядок таблиці має бути None
            row = None
        return row

    def get_model_id_name(self, u):
        # Цей метод потрібно переозначити в дочірньому класі
        """
        Визначає назву моделі та id примірника u
        :param u: примірник моделі
        :return: {'id': u.id, 'model': m, 'name': name}
        """
        try:
            m = u._meta.model_name
            m_id_n = {
                'id'    : str(u.id),
                'model' : m,
                'name'  : ""
                }
        except:
            m_id_n = {}
        return m_id_n

    def get_cell(self, u, col):
        """
        Визначає одну клітинку у двомірному масиві даних таблиці.
        :param u: примірник user
        :param col: номер колонки в таблиці (поч. з 1)
        :return cell: вміст клітинки
        """
        row = self.get_row(u)
        cell = row[col]
        return cell

    def get_cell_changes(self, old, new):
        """
        Визначає змінені клітинки в одному рядку таблиці
        шляхом порівняння старого рядка з новим
        Формат рядка:
         row[j] ,
         де j - номер колонки в таблиці (поч. з 1)
            row[0] - словник з даними про примірник:
                        {'id': f.id, 'model': m}
        :param old: старий рядок таблиці
        :param new: змінений рядок
        :return changes: словник {j: new[j], ...}
                         для всіх колонок із зміненим значенням
        """
        # print('old=', old)
        # print('new=', new)
        if new:
            changes = {}        # тут будуть змінені значення
            n = self.columnsNumber + 1 # к-сть колонок (вкл. з нульовою)
            for j in range(n):
                if j == 0:      # нульовий елемент беремо без перевірки
                    changes[j] = new.get(j)
                else:
                    if old.get(j) != new.get(j): # знайдено змінений елемент
                        changes[j] = new.get(j)
        else: # нового рядка немає
            changes = None
        return changes

    def get_supplement_data(self, f):
        # Цей метод потрібно переозначити в дочірньому класі
        # Повертає додаткові дані для передачі в шаблон через XHR,
        # які простіше отримати в Python і використати в js
        # для зміни / створення нового рядка в таблиці
        data = {}
        return data



# --------------------------------------------------
'''
# ====================================================

def get_browtable_cell_changes(old, new):
    """
    Визначає змінені клітинки в одному рядку таблиці
    шляхом порівняння старого рядка з новим
    Формат рядка:
     row[j] ,
     де j - номер колонки в таблиці (поч. з 1)
        row[0] - словник з даними про примірник:
                    {'id': f.id, 'model': m}
    :param old: старий рядок таблиці
    :param new: змінений рядок
    :return changes: словник {j: new[j], ...}
                     для всіх колонок із зміненим значенням
    """
    # print('old=', old)
    # print('new=', new)
    if new:
        changes = {}        # тут будуть змінені значення
        n = len(old)        # кількість елементів (включно з нульовим)
        for j in range(n):
            if j != 0:      # нульовий елемент не перевіряємо
                # print('j =', j, old[j], new[j])
                if old[j] != new[j]:    # знайдено змінений елемент
                    changes[j] = new[j]
                    # print('changes =', changes)
            # print('j=', j, 'changes=', changes)
    else: # нового рядка немає
        changes = None
    return changes

def get_users_table_cell(u, col):
    """
    Визначає одну клітинку у двомірному масиві даних таблиці.
    :param u: примірник user
    :param col: номер колонки в таблиці (поч. з 1)
    :return cell: вміст клітинки
    """
    row = get_users_table_row(u)
    cell = row[col]
    return cell

def get_model_id(u):
    """
    Визначає назву моделі та id примірника u
    :param u: примірник моделі
    :return: {'id': u.id, 'model': m}
    """
    m = u._meta.model_name
    model_id = {
        'id'    : str(u.id),
        'model' : m,
        'name'  : u.username
        }
    return model_id

def get_users_table_row(u):
    """
    Визначає один рядок у двомірному масиві даних таблиці.
    Формат рядка:
     row[j] - елемент словника row = {...},
     де j - номер колонки в таблиці (поч. з 1)
        row[0] - словник з даними про примірник:
                    {'id': f.id, 'model': m}
    :param u: примірник user
    :return row: одновимірний масив
    """
    if u:
        row = {}
        row[0] = get_model_id(u)
        row[1] = u.username
        row[2] = get_user_full_name(u)
        row[3] = get_user_flat_No(u)
        row[4] = u.email
        # row[5] = u.date_joined.isoformat() if u.date_joined else ""
        row[5] = u.date_joined if u.date_joined else ""
        row[6] = get_user_is_recognized(u)
        row[7] = u.is_active
        row[8] = has_group(u, 'members')
    else: # елемента нема => рядок таблиці має бути None
        row = None
    return row

def get_qs_table_array(qs, get_qs_row, sel_model_id):
    """
    Визначає двомірний масив даних таблиці.
    Формат масиву:
     arr[i][j] ,
     де i - номер рядка в таблиці (поч. з 0)
        j - номер колонки в таблиці (поч. з 1)
        arr[i][0] - словник з даними про примірник:
                    {'id': f.id, 'model': m}
    :param qs: queryset - послідовність примірників
    :param get_qs_row: функція, яка формує рядок конкретної таблиці
    :param sel_model_id: {'id': f.id, 'model': m} параметри вибраного рядка
    :return arr: 2D-масив значень таблиці + службова 0-ва колонка
    :return sel_index: порядковий номер вибраного рядка
    """
    print('get_qs_table_array:')
    arr = {}
    if sel_model_id:        # є параметри пошуку => треба шукати
        need_search = True
    else:                   # вибириємо 0 => шукати не треба
        need_search = False
    print('sel_model_id =', sel_model_id, 'need_search =', need_search)
    sel_index = 0           # зміниться, якщо буде знайдено
    i = 0
    for u in qs:
        row = get_qs_row(u)
        arr[i] = row
        if need_search:
            print('i= ', i, 'u =', 'row[0] =', row[0])
            if (sel_model_id['id'] == row[0]['id']) and \
               (sel_model_id['model'] == row[0]['model']):
                sel_index = i           # знайдено
                need_search = False
        i += 1
    return arr, sel_index


def get_users_table_array(qs, sel_model_id):
    """
    Визначає двомірний масив даних таблиці.
    Цей масив передається в шаблон синхронно при відкритті таблиці.
    Масив зберігається в невидимому полі шаблону
    і використовується для сортування таблиці
    (а також перейменування, додавання, видалення елементів)
    без перезавантаження сторінки.
    Формат масиву:
     arr[i][j] ,
     де i - номер рядка в таблиці (поч. з 0)
        j - номер колонки в таблиці (поч. з 1)
        arr[i][0] - словник з даними про примірник:
                    {'id': f.id, 'model': m}
    :param qs: queryset - послідовність примірників user
    :param sel_model_id: {'id': f.id, 'model': m} параметри вибраного рядка
    :return cap: 1D-масив заголовків таблиці
    :get_users_table_row - функція визначення рядка
    :return arr: 2D-масив значень таблиці + службова 0-ва колонка
    :return sel_index: порядковий номер вибраного рядка
    """
    # Шапка таблиці
    cap = {}
    cap[0] = ""
    cap[1] = "Логін"
    cap[2] = "Користувач"
    cap[3] = "Кв."
    cap[4] = "e-mail"
    cap[5] = "Дата ств."
    cap[6] = "Підтв."
    cap[7] = "Актив."
    cap[8] = "Чл.кооп."
    # Власне таблиця (з службовою колонкою j=0)
    arr, sel_index = get_qs_table_array(qs, get_users_table_row, sel_model_id)
    return cap, arr, sel_index



'''