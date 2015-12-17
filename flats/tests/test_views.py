from unittest.case import skip
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from flats.models import Flat, Person
from flats.views import FlatScheme, FlatDetail, AllFieldsView, FlatDetailHorizontal
import flats.views
from functional_tests_koopsite.ft_base import DummyData
from koopsite.functions import print_dict, print_list

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


@skip
class FlatSchemeTest(TestCase):
    TView = FlatScheme

    def test_flat_scheme_model(self):
        view = self.TView()
        self.assertEqual(view.model, Flat)

    def test_flat_scheme_page_renders_proper_template(self):
        response = self.client.get('/flats/scheme/')
        self.assertTemplateUsed(response, 'flats/flat_scheme.html')

    def test_get(self):
        """TView.get() gives response.status_code == 200 """
        request = RequestFactory().get('/flats/scheme/')
        view = self.TView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """TView.get_context_data() sets proper values in context."""
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
        view = self.TView()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_2(self):
        """TView.get_context_data() sets proper values in context."""
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
        view = self.TView()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)

    def test_context_data_3(self):
        """TView.get_context_data() sets proper values in context."""
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
        view = self.TView()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], d)
        self.assertEqual(context['block_length'], l)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)


# @skip
class AllFieldsViewTest(TestCase):
    # Тестуємо клас, базовий для, напр., FlatDetail

    def test_all_fields_view_attributes(self):
        view = AllFieldsView()
        self.assertEqual(view.fields, ())
        self.assertEqual(view.exclude, ('id',))

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

    def test_get_label_value_list_gives_all_fields(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        view = AllFieldsView()
        view.object = flat
        expected_obj_details = [
            ('Квартира №', '5'),
            ("Під'їзд", 2),
            ('Поверх', 1),
            ]
        obj_details = view.get_label_value_list(view.object)
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)
        # id не входить до списку
        self.assertNotIn(('id', 5), obj_details)
        # перевірка сортування
        self.assertEquals(obj_details[0], expected_obj_details[0])
        self.assertEquals(obj_details[3], expected_obj_details[1])
        self.assertEquals(obj_details[4], expected_obj_details[2])
        self.assertEquals(obj_details[4], expected_obj_details[2])
        # перевірка довжини списку
        self.assertEquals(len(obj_details), 23)

    def test_get_label_value_list_gives_some_fields(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        view = AllFieldsView()
        view.object = flat
        view.fields = ('id', 'flat_No', 'floor_No')
        expected_obj_details = [
            ('Квартира №', '5'),
            ('Поверх', 1),
            ]
        obj_details = view.get_label_value_list(view.object)
        for expected in expected_obj_details:
            self.assertIn(expected, obj_details)
        # id не входить до списку
        self.assertNotIn(('id', 5), obj_details)
        # перевірка сортування
        self.assertEquals(obj_details[0], expected_obj_details[0])
        self.assertEquals(obj_details[1], expected_obj_details[1])
        # перевірка довжини списку
        self.assertEquals(len(obj_details), 2)


    def test_get_context_data(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        kwargs = {'pk': 5}
        view = AllFieldsView()
        view = setup_view(view, request, **kwargs)
        view.model = Flat
        view.fields = ('id', 'flat_No', 'floor_No')
        view.object = flat
        expected_obj_details = [
            ('Квартира №', '5'),
            ('Поверх', 1),
            ]
        context = view.get_context_data()
        self.assertEqual(context['object_list'], expected_obj_details)

class FlatDetailTest(TestCase):

    def test_flat_detail_model_and_attributes(self):
        view = FlatDetail()
        self.assertEqual(view.model,        Flat)
        self.assertEqual(view.paginate_by,  12)
        self.assertEqual(view.exclude ,     ('id', 'flat_99'))

    def test_flat_detail_page_renders_proper_template(self):
        flat = Flat(id=5, flat_No='5')
        flat.save()
        response = self.client.get('/flats/5/')
        self.assertTemplateUsed(response, 'flats/flat_detail.html')

    def test_flat_detail_gives_response_status_code_200(self):
        flat = Flat(id=5)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        view = FlatDetail.as_view()
        response = view(request, pk=5)
        self.assertEqual(response.status_code, 200)


class FlatDetailHorizontalTest(TestCase):

    def test_flat_detail_h_model_and_attributes(self):
        view = FlatDetailHorizontal()
        self.assertEqual(view.model,        Flat)
        self.assertEqual(view.paginate_by,  0)
        self.assertEqual(view.exclude,      ('id', 'flat_99'))

    def test_flat_detail_h_page_renders_proper_template(self):
        flat = Flat(id=5, flat_No='5')
        flat.save()
        response = self.client.get('/flats/5/h/')
        self.assertTemplateUsed(response, 'flats/flat_detail_h.html')

    def test_flat_detail_h_gives_response_status_code_200(self):
        flat = Flat(id=5)
        flat.save()
        request = RequestFactory().get('/flats/5/h/')
        view = FlatDetailHorizontal.as_view()
        response = view(request, pk=5)
        self.assertEqual(response.status_code, 200)

