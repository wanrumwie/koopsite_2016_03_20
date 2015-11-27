from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from koopsite.views import index


class IndexPagetest(TestCase):

    def test_root_url_resolves_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_url_resolves_to_index_page_view(self):
        found = resolve('/index/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('koop_index.html')
        self.assertEqual(response.content.decode(), expected_html)


