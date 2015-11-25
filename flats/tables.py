from django.views.generic.list import ListView
import django_tables2 as tables
from django_tables2.views import SingleTableView
from .models import Flat, Person


class PersonTable(tables.Table):
    first_name = tables.Column()
    ln = tables.Column(accessor='last_name')
    flat_99 = tables.Column()

    class Meta:
        model = Person
        # sequence = ("selection", "first_name", "last_name")


class PersonTableView(SingleTableView):
    model = Person
    table_class = PersonTable
    template = 'flats/person_list000.html'

#===============================================================

class FlatTable000(ListView):
    model = Flat
    paginate_by = 15
    context_object_name = 'field_val'
    template_name = 'flats/flat_table.html'

    def dispatch(self, *args, **kwargs):
        return super(FlatTable000, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FlatTable, self).get_context_data(**kwargs)
        print('context=', context)
        print('self.object_list=',self.object_list)
        field_name = []
        field_val  = []
        firstiter  = True
        for flat in Flat.objects.order_by('flat_99'):
            flatval  = []
            for k in flat.fieldsList:
                if firstiter:
                    n = flat.mdbFields[k]
                    field_name.append(n)
                v = getattr(flat,k)
                try:
                    v = round(v,2)
                except:
                    pass
                flatval.append(v)
            field_val.append(flatval)
            firstiter = False
        # self.object_list = field_val
        print('='*50)
        for f in self.object_list:
            print('f=',f)
        print('='*50)
        for f in field_val:
            print('f=',f)
            for v in f:
                print(v, end=' ')
            print('-'*50)
        context['field_name']   = field_name    # назви полів
        context['field_val']    = field_val     # весь список
        return context


