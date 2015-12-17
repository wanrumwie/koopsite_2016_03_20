from unittest.case import skip
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import BaseListView, MultipleObjectMixin
from koopsite.functions import trace_print, print_list, print_dict
from koopsite.views import AllDetailView
from koopsite.views import AllRecordDetailView
from .models import Flat


class FlatList(ListView):
    model = Flat
    # paginate_by = 17
    context_object_name = 'flat_list'
    template_name = 'flats/flat_list.html'


def block_scheme():
    """
    Допоміжна функція для get_context_data()
    Групує квартири по-блочно у дворівневий словник:
    {floor0: {entrance1: [flat1, ], entrance2: [flat4, ]}, }
    :return:
    d - власне дворівневий словник списків квартир;
    floors - сортований список поверхів;
    entrances - сортований список під'їздів
    """
    # Готуємо порожні словники і списки до заповнення:
    entrances = set()
    floors = set()
    d = {}
    # Кожну квартиру з бази додаємо до списку d[f][e]
    for flat in Flat.objects.all().order_by('flat_99'):
        f = flat.floor_No
        e = flat.entrance_No
        if f not in d:
            d[f] = {}       # створюємо порожній словник для поверху
        if e not in d[f]:
            d[f][e] = []    # створюємо порожній список для блоку на поверсі
        d[f][e].append(flat)  # кожну квартиру вміщуємо у свій блок
        floors.add(f)
        entrances.add(e)
    floors = sorted(floors, reverse=True)
    entrances = sorted(entrances)
    # print(d)
    # print(floors)
    # print(entrances)
    return d, floors, entrances

def block_length(d):
    # Визначаємо для кожного під'їзду макс.к-ть квартир на поверсі
    # для того, щоб кожен під'їзд в шаблоні був представлений вертик. колонкою:
    block_length = {}
    for f in d:
        for e in d[f]:
            n = block_length.get(e, 0)
            n = max(n, len(d[f][e]))
            block_length[e] = n
    return block_length


class FlatScheme(ListView):
    model = Flat
    # context_object_name = 'flat_scheme'
    template_name = 'flats/flat_scheme.html'

    def get_context_data(self, **kwargs):
        # self.object_list = Flat.objects.all()
        self.object_list = None
        # Створюємо атрибут класу self.object_list
        # інакше TestCase дає AttributeError:
        #   'FlatScheme' object has no attribute 'object_list'
        # Крім того при None в контекст не передається (двічі!)
        # непотрібний тут список всіх об'єктів.
        # Всі потрібні значення описані нижче:
        kwargs = super(FlatScheme, self).get_context_data(**kwargs)
        d, floors, entrances = block_scheme()
        l = block_length(d)
        kwargs['block_scheme'] = d
        kwargs['block_length'] = l
        kwargs['floors']       = floors
        kwargs['entrances']    = entrances
        # print_dict(kwargs, 'kwargs')
        return kwargs


class AllFieldsView(MultipleObjectMixin, DetailView):
    """
    Базовий CBV для відображення ВСІХ полів одного запису моделі.
    Успадкування від DetailView дозволяє отримати pk з url_conf
    і сам об'єкт, який передасться у складі контексту у шаблон
    під іменем object .
    Успадкування від MultipleObjectMixin дозволяє використати
    розбиття на сторінки списку. Сам список object_list формується
    методом get_label_value_list(self, obj) і охоплює всі поля моделі
    у заданому порядку.
    При необхідності змінити імена об'єкта і списку його деталей
    потрібно переозначити метод get_context_data(self, **kwargs),
    дописавши в нього щось на зразок context['flat'] = self.object
    та/або context['flat_details'] = self.object_list .
    """
    fields  = ()        # Поля, які будуть виведені. Якщо порожній, то всі.
    exclude = ('id',)   # Поля, які виключаються із списку виводу.
    # Наступні змінні будуть визначені в наслідуваному класі, наприклад:
    # model = Report
    # per_page = 12
    # template_name = 'folders/report_detail.html'

    def val_repr(self, v, decimal=2):
        """
        Представлення значення у шаблоні.
        Заокруглює число. Для нуля повертає "".
        Не винесена в модуль functions.py , щоб у дочірньому класі
        можна було її переозначити.
        """
        # TODO-поверх 0 втводиться як "" - виправити!
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

    # def get_label_value_list(self, obj):
    #     keys = []
    #     if self.fields:
    #         for k in self.fields:
    #             f = obj._meta.get_field(k)
    #             n = f.verbose_name
    #             if k not in self.exclude: keys.append((k, n))
    #     else:
    #         for f in obj._meta.fields:
    #             k = f.name
    #             n = f.verbose_name
    #             if k not in self.exclude: keys.append((k, n))
    #     obj_details = []
    #     for k, n in keys:
    #         v = getattr(self.object,k)
    #         v = self.val_repr(v, 2)
    #         obj_details.append((n, v))
    #     return obj_details

    def get_context_data(self, **kwargs):
        key_list, verbname_list = self.get_field_keys_verbnames()
        value_list = self.get_value_list(self.object, key_list)
        self.object_list = self.get_label_value_list(verbname_list, value_list)
        # self.object_list = self.get_label_value_list(self.object)
        context = super(AllFieldsView, self).get_context_data(**kwargs)
        # print_list(key_list, name='key_list')
        # print_list(verbname_list, name='vn_list')
        # print_list(value_list, name='value_list from model')
        # print_list(nv_list, name='label_value_list from model')
        # print('context :------------------------')
        # print_dict(context, 'contenxt')
        return context


class FlatDetail(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    paginate_by = 12
    exclude = ('id', 'flat_99')   # Поля, які виключаються із списку виводу.


class FlatDetailHorizontal(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail_h.html'
    paginate_by = 0
    exclude = ('id', 'flat_99')   # Поля, які виключаються із списку виводу.


class FlatTable(AllRecordDetailView):
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

