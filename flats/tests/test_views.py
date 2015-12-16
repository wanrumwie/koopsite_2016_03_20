from unittest.case import skip
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from flats.models import Flat, Person
from flats.views import FlatScheme, FlatDetail, AllFieldsView
import flats.views
from folders.models import Folder
from folders.views import FolderDetail
from functional_tests_koopsite.ft_base import DummyData
from koopsite.functions import print_dict, print_list
from koopsite.views import index

def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``
    http://tech.novapost.fr/django-unit-test-your-views-en.html
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class FlatSchemeTest(TestCase):

    def test_flat_scheme_model(self):
        view = FlatScheme()
        self.assertEqual(view.model, Flat)

    def test_flat_scheme_page_renders_proper_template(self):
        response = self.client.get('/flats/scheme/')
        self.assertTemplateUsed(response, 'flats/flat_scheme.html')

    def test_get(self):
        """FlatScheme.get() gives response.status_code == 200 """
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """FlatScheme.get_context_data() sets proper values in context."""
        # Імітуємо будинок з одної квартири:
        floors=[0]
        entrances=[1]
        flat = Flat(floor_No=0, entrance_No=1)
        flat.save()
        block_scheme = {0: {1: [flat, ]}}
        # {0: {1: [flat, ], 2: [flat, ]}, 1: {1: [flat, ], 2: [flat, ]},}
        block_length = {1: 1}
        kwargs = {}
        kwargs['block_scheme'] = block_scheme
        kwargs['block_length'] = block_length
        kwargs['floors']       = floors
        kwargs['entrances']    = entrances
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_2(self):
        """FlatScheme.get_context_data() sets proper values in context."""
        # Імітуємо будинок з кількох квартир:
        flat1 = Flat(floor_No=1, entrance_No=1)
        flat1.save()
        flat2 = Flat(floor_No=2, entrance_No=2)
        flat2.save()
        flat3 = Flat(floor_No=2, entrance_No=2)
        flat3.save()
        floors=[2,1]
        entrances=[1,2]
        block_scheme = {1: {1: [flat1]}, 2: {2: [flat2, flat3]}}
        # {0: {1: [flat, ], 2: [flat, ]}, 1: {1: [flat, ], 2: [flat, ]},}
        block_length = {1: 1, 2: 2}
        kwargs = {}
        kwargs['block_scheme'] = block_scheme
        kwargs['block_length'] = block_length
        kwargs['floors']       = floors
        kwargs['entrances']    = entrances
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_3(self):
        """FlatScheme.get_context_data() sets proper values in context."""
        # Імітуємо будинок з кількох квартир:
        floors=(1,2)
        entrances=(1,2)
        DummyData().create_dummy_building(floors=floors, entrances=entrances)
        d, floors, entrances = flats.views.block_scheme()
        l = flats.views.block_length(d)
        kwargs = {}
        kwargs['block_scheme'] = d
        kwargs['block_length'] = l
        kwargs['floors']       = floors
        kwargs['entrances']    = entrances
        # print_dict(kwargs, 'kwargs')
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], d)
        self.assertEqual(context['block_length'], l)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)


class AllFieldsViewTest(TestCase):
    # Тестуємо клас, базовий для, напр., FlatDetail

    def test_all_fields_view_attributes(self):
        view = AllFieldsView()
        self.assertEqual(view.keylist    , [])
        self.assertEqual(view.namedict   , {})
        self.assertEqual(view.valfunction, round)
        self.assertEqual(view.fargs      , (2,))
        self.assertEqual(view.fkwargs    , {})
        self.assertEqual(view.url_name   , '')
        self.assertEqual(view.context_object_name, 'obj_details')
        self.assertEqual(view.context_obj_name, 'obj')

    def test_get_context_obj_name_return_self(self):
        view = AllFieldsView()
        view.context_obj_name = 'CON'
        view.model = Flat
        obj = Flat()
        self.assertEqual(view.get_context_obj_name(obj), 'CON')

    def test_get_context_obj_name_return_obj_meta_model_name(self):
        view = AllFieldsView()
        view.context_obj_name = ''
        view.model = Flat
        obj = Person()
        self.assertEqual(view.get_context_obj_name(obj), 'person')

    def test_get_context_obj_name_return_none(self):
        view = AllFieldsView()
        view.context_obj_name = ''
        view.model = Flat
        obj = [1,2,3]
        self.assertEqual(view.get_context_obj_name(obj), None)

    def test_get_context_obj_name_return_none_2(self):
        view = AllFieldsView()
        view.context_obj_name = ''
        view.model = None
        obj = Flat
        self.assertEqual(view.get_context_obj_name(obj), None)

    def test_val_repr(self):
        view = AllFieldsView()
        self.assertEqual(view.val_repr(5), 5)
        self.assertEqual(view.val_repr(5.1), 5.1)
        self.assertEqual(view.val_repr(5.12), 5.12)
        self.assertEqual(view.val_repr(5.123), 5.12)
        self.assertEqual(view.val_repr(5.126), 5.13)
        self.assertEqual(view.val_repr(5.126, 1), 5.1)
        self.assertEqual(view.val_repr(0), "")
        self.assertEqual(view.val_repr("qwe"), "qwe")

    def test_get_label_value_list(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        view = AllFieldsView()
        view.obj = flat

        # Має вийти несортований список [(n, v),...], де n - obj.__dict__
        view.keylist = []
        view.namedict = []
        expected_obj_details = [
            ('id', 5),
            ('flat_No', '5'),
            ('entrance_No', 2),
            ('floor_No', 1),
            ]
        obj_details = view.get_label_value_list(view.obj)
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)

        # Має вийти список [(n, v),...], сортований так як keylist - спеціально описаний в моделі
        view.keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
        # view.namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
        expected_obj_details = [
            ('flat_No', '5'),
            ('entrance_No', 2),
            ('floor_No', 1),
            ]
        obj_details = view.get_label_value_list(view.obj)
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)
        # id не входить до списку keylist
        self.assertNotEquals(('id', 5), obj_details)
        # перевірка сортування
        self.assertEquals(expected_obj_details[0], obj_details[0])
        self.assertEquals(expected_obj_details[1], obj_details[3])
        self.assertEquals(expected_obj_details[2], obj_details[4])

        # Має вийти список [(n, v),...], сортований так як keylist - спеціально описаний в моделі
        # з укр.назвами полів з словника namedict, описаного в моделі
        # view.keylist = Flat.fieldsList   # список полів, спеціально описаний в моделі
        view.namedict = Flat.mdbFields   # укр.назви полів, описані в моделі
        expected_obj_details = [
            ('Квартира №', '5'),
            ("Під'їзд", 2),
            ('Поверх', 1),
            ]
        obj_details = view.get_label_value_list(view.obj)
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)
        # id не входить до списку keylist
        self.assertNotEquals(('id', 5), obj_details)
        # перевірка сортування
        self.assertEquals(expected_obj_details[0], obj_details[0])
        self.assertEquals(expected_obj_details[1], obj_details[3])
        self.assertEquals(expected_obj_details[2], obj_details[4])
        self.assertEquals(expected_obj_details[2], obj_details[4])


    # TODO-використати flat._meta.fields.name і ...verbose_name
    #     print('flat._meta.fields =', flat._meta.fields)
    #     for f in flat._meta.fields:
    #         print('-'*20)
    #         print_dict(f.__dict__, name=f.name)

    def test_get_queryset(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        view = AllFieldsView()
        view.obj = flat
        view.model = Flat
        view.id = 5

        # Має вийти несортований список [(n, v),...], де n - obj.__dict__
        # view.keylist = []
        # view.namedict = []
        expected_obj_details = [
            ('id', 5),
            ('flat_No', '5'),
            ('entrance_No', 2),
            ('floor_No', 1),
            ]
        obj_details = view.get_queryset()
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)

    '''
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()

    '''

    def test_get(self):
        flat = Flat(id=5)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        kwargs = {'pk': 5}
        view = AllFieldsView()
        view = setup_view(view, request, **kwargs)
        view.model = Flat
        view.get(request, **kwargs)
        # response = view.as_view(request)
        self.assertEqual(view.id, 5)

    def test_get_context_data(self):
        flat = Flat(id=5)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        kwargs = {'pk': 5}
        view = AllFieldsView()
        view = setup_view(view, request, **kwargs)
        view.model = Flat
        view.id = 5
        view.context_obj_name = 'CON'
        view.object_list = view.get_queryset() # емулюємо роботу view.get()
        context = view.get_context_data()
        print_dict(context, 'context')
        self.assertEqual(context['CON'], flat)


class FlatDetailTest(TestCase):

    def test_flat_detail_model_and_attributes(self):
        view = FlatDetail()
        self.assertEqual(view.model,    Flat)
        self.assertEqual(view.per_page, 12)
        self.assertEqual(view.keylist , Flat.fieldsList)
        self.assertEqual(view.namedict, Flat.mdbFields)
        self.assertEqual(view.context_obj_name, 'flat')

    def test_flat_detail_page_renders_proper_template(self):
        flat = Flat(id=5, flat_No='5')
        flat.save()
        response = self.client.get('/flats/5/')
        self.assertTemplateUsed(response, 'flats/flat_detail.html')

    def test_get(self):
        """FlatDetail.get() gives response.status_code == 200 """
        flat = Flat(id=5)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        view = FlatScheme.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
