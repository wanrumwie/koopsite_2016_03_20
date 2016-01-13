from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from flats.models import Flat
from koopsite.views import index, AllFieldsView, AllRecordsAllFieldsView


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



# @skip
class AllFieldsViewTest(TestCase):
    # Тестуємо клас, базовий для, напр., FlatDetail

    def test_attributes(self):
        view = AllFieldsView()
        self.assertIsNone(view.context_self_object_name)
        self.assertIsNone(view.context_object_name)

    def test_get_context_data(self):
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        request = RequestFactory().get('/flats/5/')
        kwargs = {'pk': 5}
        view = AllFieldsView()
        view = setup_view(view, request, **kwargs)
        view.model = Flat
        view.fields = ('id', 'flat_No', 'floor_No')
        view.exclude = ('id', )
        view.object = flat
        expected_obj_details = [
            ('Квартира №', '5'),
            ('Поверх', 1),
            ]
        context = view.get_context_data()
        self.assertEqual(context['object_list'], expected_obj_details)


class AllRecordsAllFieldsViewTest(TestCase):
    # Тестуємо клас, базовий для, напр., FlatTable

    def test_get_context_verbose_list_name(self):
        view = AllRecordsAllFieldsView()
        self.assertEqual(view.context_verbose_list_name, "field_names")

    def test_get_queryset(self):
        flat = Flat(id=1, flat_99=1, flat_No='1', floor_No=1, entrance_No=1)
        flat.save()
        flat = Flat(id=2, flat_99=2, flat_No='2', floor_No=2, entrance_No=2)
        flat.save()
        flat = Flat(id=3, flat_99=3, flat_No='3', floor_No=3, entrance_No=3)
        flat.save()
        view = AllRecordsAllFieldsView()
        view.model = Flat
        view.fields = ('id', 'flat_No', 'floor_No', 'entrance_No')
        view.exclude = ('id', )
        expected = [['1', 1, 1], ['2', 2, 2], ['3', 3, 3]]
        self.assertEqual(view.get_queryset(), expected)

    # @skip
    def test_get_context_data(self):
        flat = Flat(id=1, flat_99=1, flat_No='1', floor_No=1, entrance_No=1)
        flat.save()
        flat = Flat(id=2, flat_99=2, flat_No='2', floor_No=2, entrance_No=2)
        flat.save()
        flat = Flat(id=3, flat_99=3, flat_No='3', floor_No=3, entrance_No=3)
        flat.save()

        request = RequestFactory().get('/flats/table/')
        kwargs = {
            'object_list' : [['1', 1, 1], ['2', 2, 2], ['3', 3, 3]]
        }
        view = AllRecordsAllFieldsView()
        view = setup_view(view, request, **kwargs)
        # view = AllRecordsAllFieldsView.as_view()
        view.model = Flat
        view.object_list = None # Означуємо атрибут, бо інкаше тест видасть помилку:
                                # File "C:\Python34\lib\site-packages\django-1.8.2-py3.4.egg\django\views\generic\list.py", line 130, in get_context_data
                                #     queryset = kwargs.pop('object_list', self.object_list)
                                # AttributeError: 'AllRecordsAllFieldsView' object has no attribute 'object_list'
        view.context_verbose_list_name = 'title_list'
        view.fields = ('id', 'flat_No', 'floor_No', 'entrance_No')
        view.exclude = ('id', )
        expected = [['1', 1, 1], ['2', 2, 2], ['3', 3, 3]]
        exp_verb = ['Квартира №', 'Поверх', "Під'їзд"]
        context = view.get_context_data(**kwargs)
        self.assertEqual(context['object_list'], expected)
        self.assertEqual(context['title_list'], exp_verb)





class IndexPageTest(TestCase):

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

    def test_index_page_renders_proper_template(self):
        response = self.client.get('/index/')
        self.assertTemplateUsed(response, 'koop_index.html')

