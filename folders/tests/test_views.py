from unittest.case import skip
from datetime import timedelta
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve, reverse
from django.http.request import HttpRequest
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.html import escape
from django.utils.timezone import now
from folders.forms import FolderForm, FolderFormInFolder
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder
from folders.views import FolderCreate, FolderList, FolderDetail, ReportList, ReportDetail, ReportPreview, \
    FolderCreateInFolder
from koopsite.settings import LOGIN_URL
from koopsite.tests.test_base import DummyUser


class FolderListTest(TestCase):

    def setUp(self):
        self.cls_view = FolderList
        self.path = '/folders/list/'
        self.template = 'folders/folder_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.paginate_by, 5)
        self.assertEqual(view.ordering, 'name')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FolderDetailTest(TestCase):

    def setUp(self):
        self.cls_view = FolderDetail
        self.path = '/folders/1/'
        self.template = 'folders/folder_detail.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.paginate_by, 12)
        self.assertEqual(view.context_self_object_name, 'folder')
        self.assertEqual(view.context_object_name, 'obj_details')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        DummyFolder().create_dummy_root_folder()
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        DummyFolder().create_dummy_root_folder()
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))
        # Перевіряємо response.url.startswith(), бо перевірка:
        # self.assertRedirects(response, LOGIN_URL)
        # дає помилку:
        # AttributeError: 'HttpResponseRedirect' object has no attribute 'client'

    def test_view_gives_response_status_code_200(self):
        DummyFolder().create_dummy_root_folder()
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class ReportListTest(TestCase):

    def setUp(self):
        self.cls_view = ReportList
        self.path = '/folders/report/list/'
        self.template = 'folders/report_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.ordering, 'filename')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class ReportDetailTest(TestCase):

    def setUp(self):
        self.cls_view = ReportDetail
        self.path = '/folders/report/1/'
        self.template = 'folders/report_detail.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)
        self.assertEqual(view.paginate_by, 12)
        self.assertEqual(view.context_self_object_name, 'report')
        self.assertEqual(view.context_object_name, 'obj_details')

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class ReportPreviewTest(TestCase):

    def setUp(self):
        self.cls_view = ReportPreview
        self.path = '/folders/report/1/preview/'
        self.template = 'folders/report_preview.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Report)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        root = DummyFolder().create_dummy_root_folder()
        DummyFolder().create_dummy_report(root)
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)


class FolderCreateTest(TestCase):

    def setUp(self):
        self.cls_view = FolderCreate
        self.path = '/folders/create/'
        self.template = 'folders/folder_create.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderForm)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_simple_User(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        root = DummyFolder().create_dummy_root_folder()
        data = {
            'name' : 'dummy_folder_post',
        }
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        response = self.cls_view.as_view()(request)
        self.assertEqual(response.status_code, 302)
        # Витягаємо з бази щойно створений запис:
        f = self.cls_view.model.objects.last()
        self.assertEqual(f.name, data['name'])
        expected_url = f.get_absolute_url()
        self.assertEqual(response.url, expected_url)



class FolderCreateInFolderTest(TestCase):

    def setUp(self):
        self.cls_view = FolderCreateInFolder
        self.path = '/folders/1/create/'
        self.template = 'folders/folder_create.html'
        self.parent_folder = DummyFolder().create_dummy_root_folder()

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model, Folder)
        self.assertEqual(view.form_class, FolderFormInFolder)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_no_template_AnonymousUser(self):
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_no_template_simple_user(self):
        DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get(self.path)
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(response, self.template)

    def test_view_renders_proper_template(self):
        dummy_user = DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_simple_User(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # def test_get(self):
    #     dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
    #     self.client.login(username='fred', password='secret')
    #     DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
    #     request = RequestFactory().get(self.path)
    #     request.user = dummy_user
    #     kwargs = {'parent': 1}
    #     response = self.cls_view.as_view()(request, **kwargs)
    #     self.assertEqual(response.status_code, 200)
    #
    def test_post(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        data = {
            'name' : 'dummy_folder_post'
        }
        request = RequestFactory().post(self.path, data)
        request.user = dummy_user
        kwargs = {'parent': 1}
        response = self.cls_view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, "/folders/1/contents/")
        # Витягаємо з бази щойно створений запис:
        f = self.cls_view.model.objects.last()
        # Перевіряємо поля:
        self.assertEqual(f.name, data['name'])
        self.assertEqual(f.parent, self.parent_folder)
        # Час створення (до секунди) співпадає з поточним?
        self.assertAlmostEqual(f.created_on, now(), delta=timedelta(minutes=1))
        expected_url = self.parent_folder.get_absolute_url()
        # expected_url = reverse('folders:folder-contents', {'pk': self.parent_folder.id})
        self.assertEqual(response.url, expected_url)

