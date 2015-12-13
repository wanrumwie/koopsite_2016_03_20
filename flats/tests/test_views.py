from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
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

    # def test_flat_scheme_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     view = FlatScheme.as_view()
    #     response = view(request)
    #     expected_html = render_to_string('flat_scheme.html')
    #     self.assertEqual(response.content.decode(), expected_html)
    #
    # def test_flat_scheme_url_resolves_to_proper_page_view(self):
    #     found = resolve('/flats/scheme/')
    #     view = FlatScheme.as_view()
    #     self.assertEqual(found.func, view)

    def test_get(self):
        """FlatScheme.get() sets 'name' in response context."""
        # Setup request and view.
        request = RequestFactory().get('/flats/scheme/')
        view = FlatScheme.as_view()
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'flats/flat_scheme.html')

    def test_context_data(self):
        """FlatScheme.get_context_data() sets proper values in context."""
        entrances=(1,2,3,4,5,6)
        floors=(0,1,2,3,4,5)
        block_scheme = 'dummy_block_scheme'
        block_length = 1256
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


'''

'''
