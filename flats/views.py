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
    exclude = ['id',]   # Поля, які виключаються із списку виводу.
    keylist = []        # Список полів, які буде виведено.
                        # Якщо пустий, то список полів буде __dict__
    namedict = {}       # Словник укр.назв полів, які буде виведено.
                        # Якщо пустий, то назви будуть взяті з keylist
    valfunction = round # Функція обробки значення поля (напр. round)
    fargs = (2,)        # список аргументів функції f(v, *fargs)
    fkwargs = {}        # словник аргументів функції f(v, **fkwargs)
    url_name = ''       # параметр name в url(), який є основним для
                        # даного DetailView (ще без сторінок)
    # Наступні змінні будуть визначені в наслідуваному класі, наприклад:
    # model = Report
    # per_page = 12
    # template_name = 'folders/report_detail.html'

    def val_repr(self, v, decimal=2):
        """
        Заокруглює число. Для нуля повертає "".
        """
        try:    v = round(v, decimal)
        except: pass
        if v == 0: v = ""
        return v

    #     print('flat._meta.fields =', flat._meta.fields)
    #     for f in flat._meta.fields:
    #         print('-'*20)
    #         print_dict(f.__dict__, name=f.name)
    def get_label_value_list(self, obj):
        print('flat._meta.fields =', obj._meta.fields)
        keys = []
        for f in obj._meta.fields:
            k = f.name
            if k not in self.exclude: keys.append(k)
            print(k)
            # print('%-20s %s' % (f.name, f.verbose_name))
        obj_details = []
        # keylist = [f.name for f in self.object._meta.fields]
        # keylist = self.keylist #or keylist
        keylist = keys
        for k in keylist:
            try:    n = self.namedict[k]
            except: n = k
            v = getattr(self.object,k)
            v = self.val_repr(v, 2)
            obj_details.append((n, v))
        return obj_details

    # def get_label_value_list(self, obj):
    #     obj_details = []
    #     keylist = self.keylist or self.object.__dict__
    #     for k in keylist:
    #         try:    n = self.namedict[k]
    #         except: n = k
    #         v = getattr(self.object,k)
    #         v = self.val_repr(v, 2)
    #         obj_details.append((n, v))
    #     return obj_details

    def get_context_data(self, **kwargs):
        self.object_list = self.get_label_value_list(self.object)
        context = super(AllFieldsView, self).get_context_data(**kwargs)
        print('context :------------------------')
        print_dict(context, 'contenxt')
        return context


class FlatDetail(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    paginate_by = 12
    keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
    namedict = Flat.mdbFields   # укр.назви полів, описані в моделі


class FlatDetailHorizontal(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail_h.html'
    paginate_by = 0
    keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
    namedict = Flat.mdbFields   # укр.назви полів, описані в моделі


class FlatTable(AllRecordDetailView):
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

