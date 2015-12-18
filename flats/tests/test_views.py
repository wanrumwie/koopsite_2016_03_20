from unittest.case import skip
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from flats.models import Flat, Person
from flats.views import FlatScheme, FlatDetail, \
                        FlatDetailHorizontal, FlatList, FlatTable
import flats.views
from functional_tests_koopsite.ft_base import DummyData
from koopsite.functions import print_dict, print_list

# @skip
from koopsite.tests.test_views import setup_view


class FlatSchemeTest(TestCase):
    TView = FlatScheme

    def test_flat_scheme_model(self):
        view = FlatScheme()
        self.assertEqual(view.model, Flat)

    def test_flat_scheme_page_renders_proper_template(self):
        response = self.client.get('/flats/scheme/')
        self.assertTemplateUsed(response, 'flats/flat_scheme.html')

    def test_flat_scheme_gives_response_status_code_200(self):
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme.as_view()
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
        # TODO-
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
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['block_scheme'], d)
        self.assertEqual(context['block_length'], l)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['entrances']   , entrances)


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


class FlatListTest(TestCase):

    def test_flat_list_model_and_attributes(self):
        view = FlatList()
        self.assertEqual(view.model,                Flat)
        self.assertEqual(view.context_object_name , 'flat_list')

    def test_flat_list_page_renders_proper_template(self):
        response = self.client.get('/flats/list/')
        self.assertTemplateUsed(response, 'flats/flat_list.html')

    def test_flat_list_gives_response_status_code_200(self):
        request = RequestFactory().get('/flats/list/')
        view = FlatList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FlatTableTest(TestCase):

    def test_flat_table_model_and_attributes(self):
        view = FlatTable()
        self.assertEqual(view.model, Flat)
        self.assertEqual(view.paginate_by, 15)
        self.assertEqual(view.exclude, ('id', 'flat_99'))
        self.assertEqual(view.context_object_name , "field_val")
        self.assertEqual(view.context_verbose_list_name, "field_name")

    def test_flat_table_page_renders_proper_template(self):
        response = self.client.get('/flats/table/')
        self.assertTemplateUsed(response, 'flats/flat_table.html')

    def test_flat_table_gives_response_status_code_200(self):
        request = RequestFactory().get('/flats/table/')
        view = FlatTable.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

