from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from flats.models import Flat
from flats.views import FlatScheme
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
        floors=[1,2]
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

