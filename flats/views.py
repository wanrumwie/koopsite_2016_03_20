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


class FlatDetail(AllDetailView):
    model = Flat
    template_name = 'flats/flat_detail.html'
    per_page = 12
    keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
    namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
    url_name='flat-detail'


class FlatDetailHorizontal(FlatDetail):
    template_name = 'flats/flat_detail_h.html'
    per_page = 0


class FlatTable(AllRecordDetailView):
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

