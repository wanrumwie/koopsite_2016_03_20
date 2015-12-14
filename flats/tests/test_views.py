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

    def test_flat_scheme_page_renders_proper_template(self):
        response = self.client.get('/flats/scheme/')
        self.assertTemplateUsed(response, 'flats/flat_scheme.html')

    def test_get(self):
        """FlatScheme.get() gives response.status_code == 200 """
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme.as_view()
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.template_name[0], 'flats/flat_scheme.html')

    def test_context_data(self):
        """FlatScheme.get_context_data() sets proper values in context."""
        # Імітуємо будинок з одної квартири:
        entrances=[1]
        floors=[0]
        flat = Flat(floor_No=0, entrance_No=1)
        flat.save()
        block_scheme = {0: {1: [flat, ]}}
        # {0: {1: [flat, ], 2: [flat, ]}, 1: {1: [flat, ], 2: [flat, ]},}
        block_length = {1: 1}
        kwargs = {}
        kwargs['block_scheme'] = block_scheme
        kwargs['block_length'] = block_length
        kwargs['entrances']    = entrances
        kwargs['floors']       = floors
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme()
        view = setup_view(view, request, kwargs)
        # Run.
        context = view.get_context_data()
        # Check.
        self.assertEqual(context['entrances']   , entrances)
        self.assertEqual(context['floors']      , floors)
        self.assertEqual(context['block_scheme'], block_scheme)
        self.assertEqual(context['block_length'], block_length)

