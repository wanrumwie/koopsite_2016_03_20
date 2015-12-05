from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape
from folders.models import Folder
from folders.views import FolderCreate, FolderList


class FolderCreateViewTest(TestCase):

    def test_url_resolves_to_proper_view(self):
        found = resolve('/folders/create/')
        self.assertEqual(found.func.__name__, FolderCreate.__name__) #

    # def test_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = FolderCreate.get(request)
    #     expected_html = render_to_string(FolderCreate.template_name)
    #     self.assertEqual(response.content.decode(), expected_html)

    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)


