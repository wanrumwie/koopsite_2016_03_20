from django.views.generic import ListView, DetailView
from koopsite.views import AllDetailView
from koopsite.views import AllRecordDetailView
from .models import Flat


class FlatList(ListView):
    model = Flat
    # paginate_by = 17
    context_object_name = 'flat_list'
    template_name = 'flats/flat_list.html'


def block_scheme():
    # фомування вкладеного списку квартир - список блоків.
    # Блок - це квартири на одній сходовій клітці.
    # [floor0, floor1, ... floor5]
    # floor1 = [block1, block2, ... block6]
    # block1 = [flat1, flat2, flat3]
    # У результаті матимемо список:
    # block = [ [ [flat1, flat2, flat3], ... ] , [ [ ... ], ... ] ... ]
    block_list = []
    for y in range(6):      # формуємо для кожного блоку поч.знач.: - []
        floor = 5 - y
        block_list.append([])
        block_list[y] = []
        for x in range(6):
            entr = x + 1
            block_list[y].append([])
    for f in Flat.objects.all().order_by('flat_99'):
        y = 5 - f.floor_No
        x = f.entrance_No - 1
        block_list[y][x].append(f)  # кожну квартиру вміщуємо у свій блок
    for y in [5]:
        for x in [0,1,2]:
            for i in range(3):
                block_list[y][x].append(None)   # блоки без квартир
    return block_list


class FlatScheme(ListView):
    model = Flat
    context_object_name = 'flat_list'
    template_name = 'flats/flat_scheme.html'

    def get_context_data(self, **kwargs):
        context = super(FlatScheme, self).get_context_data(**kwargs)
        context['block_list']       = block_scheme()
        context['entrance_list']    = list(range(1,7))
        print("context['block_list'] =", context['block_list'])
        return context



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

    context_object_name = 'obj_details' # назва queryset, що йде в шаблон
                                        # {% for k, v in obj_details %}
    context_obj_name    = 'obj'         # назва об'єкта, що йде в шаблон

    def get_context_obj_name(self, obj):
        """
        Дає назву obj, чиї поля зібрані в queryset.
        Функція зроблена за аналогією до get_context_object_name з ListView
        """
        if self.context_obj_name:
            s = self.context_obj_name
        elif self.model:
            try: s =  obj._meta.model_name
            except: s = None
        else:
            s = None
        return s

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        return super(AllFieldsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        self.obj = self.model.objects.get(id=self.id)
        obj_details = []
        keylist = self.keylist or self.obj.__dict__
        for k in keylist:
            try:    n = self.namedict[k]
            except: n = k
            v = getattr(self.obj,k)
            if self.valfunction:
                try:    v = self.valfunction(v, *self.fargs, **self.fkwargs)
                        # Замість v = round(v,2) або v = round(v,ndigits=2)
                except: pass
            if v == 0: v = ""
            obj_details.append((n, v))
        return obj_details

    def get_context_data(self, **kwargs):
        context = super(AllFieldsView, self).get_context_data(**kwargs)
        context_obj_name = self.get_context_obj_name(self.obj)
        context[context_obj_name]  = self.obj
        print('context :------------------------')
        for k,v in context.items():
            print('%20s : %s' % (k, v))
        return context



class FlatDetail(AllFieldsView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    per_page = 12
    keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
    namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
    url_name='flat-detail'
    context_obj_name    = 'flat' # назва об'єкта, що йде в шаблон


# class FlatDetail(AllDetailView):
#     model = Flat
#     template_name = 'flats/flat_detail.html'
#     per_page = 12
#     keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
#     namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
#     url_name='flat-detail'
#
#
class FlatDetailHorizontal(FlatDetail):
    template_name = 'flats/flat_detail_h.html'
    per_page = 0


class FlatTable(AllRecordDetailView):
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

