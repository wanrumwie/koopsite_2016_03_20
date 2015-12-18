from unittest.case import skip
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import BaseListView, MultipleObjectMixin
from koopsite.functions import trace_print, print_list, print_dict, AllFieldsMixin
from koopsite.views import AllDetailView, AllFieldsView, AllRecordsAllFieldsView
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


class FlatTable(AllRecordsAllFieldsView):
    model = Flat
    paginate_by = 15
    exclude = ('id', 'flat_99')   # Поля, які виключаються із списку виводу.
    template_name = 'flats/flat_table.html'
    context_object_name = "field_val"
    context_verbose_list_name = "field_name"

