from unittest.case import skip
from django.views.generic import ListView, DetailView
from django.views.generic.list import BaseListView
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


class AllFieldsView(ListView):
    # CBV для виводу всіх полів одного запису моделі
    keylist = []            # Список полів, які буде виведено.
                            # Якщо пустий, то список полів буде __dict__
    namedict = {}           # Словник укр.назв полів, які буде виведено.
                            # Якщо пустий, то назви будуть взяті з keylist
    valfunction = round     # Функція обробки значення поля (напр. round)
    fargs = (2,)            # список аргументів функції f(v, *fargs)
    fkwargs = {}            # словник аргументів функції f(v, **fkwargs)
    url_name = ''           # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)
    # Наступні змінні будуть визначені в наслідуваному класі:
    # model = Report
    # template_name = 'folders/report_detail.html'
    # per_page = 12

    context_obj_name    = 'obj'         # назва об'єкта, чиї деталі йдуть в шаблон
    context_object_name = 'obj_details' # назва списку, що йде в шаблон
                                        # {% for k, v in obj_details %}

    def val_repr(self, v, decimal=2):
        """
        Заокруглює число. Для нуля повертає "".
        """
        try:    v = round(v, decimal)
        except: pass
        if v == 0: v = ""
        return v

    def get_label_value_list(self, obj):
        obj_details = []
        keylist = self.keylist or self.obj.__dict__
        for k in keylist:
            try:    n = self.namedict[k]
            except: n = k
            v = getattr(self.obj,k)
            v = self.val_repr(v, 2)
            obj_details.append((n, v))
        return obj_details

    def get_context_obj_name(self, obj):
        """
        Дає назву obj, чиї поля зібрані в queryset.
        Функція зроблена за аналогією до get_context_object_name з ListView
        """
        if self.context_obj_name:
            s = self.context_obj_name
        elif self.model:
            try:    s =  obj._meta.model_name
            except: s = None
        else:
            s = None
        return s

    def get(self, request, *args, **kwargs):
        print('kwargs =', kwargs)
        self.id = kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        print('self.id =', self.id)
        print('self.model =', self.model)
        a = self.model.objects.all()
        print('a =', a)
        self.obj = self.model.objects.get(id=self.id)
        print('self.obj =',self.obj)
        return super(AllFieldsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        obj_details = self.get_label_value_list(self.obj)
        return obj_details

    def get_context_data(self, **kwargs):
        # print('get_context_data: self.object_list =', self.object_list)
        # print('get_context_data: self.obj =', self.obj)
        # print('get_context_data: self.obj =', self.obj.__dict__)
        context = super(AllFieldsView, self).get_context_data(**kwargs)
        context_obj_name = self.get_context_obj_name(self.obj)
        context[context_obj_name]  = self.obj
        # print('context :------------------------')
        # print_dict(context, 'contenxt')
        return context



class FlatDetail(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    paginate_by = 12
    keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
    namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
    url_name='flat-detail'
    context_obj_name    = 'flat' # назва об'єкта, що йде в шаблон


class FlatDetailHorizontal(FlatDetail):
    template_name = 'flats/flat_detail_h.html'
    paginate_by = 0
    url_name='flat-detail-h'


class FlatTable(AllRecordDetailView):
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

