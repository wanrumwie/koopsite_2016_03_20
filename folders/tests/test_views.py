from unittest.case import skip
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.html import escape
from folders.forms import FolderForm, FolderFormInFolder
from folders.models import Folder, Report
from folders.tests.test_base import DummyFolder
from folders.views import FolderCreate, FolderList, FolderDetail, ReportList, ReportDetail, ReportPreview, \
    FolderCreateInFolder
from koopsite.tests.test_base import DummyUser
from koopsite.tests.test_views import setup_view


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

    def test_view_gives_response_status_code_302_simple_User(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class FolderCreateInFolderTest(TestCase):

    def setUp(self):
        self.cls_view = FolderCreateInFolder
        self.path = '/folders/1/create/'
        self.template = 'folders/folder_create.html'

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

    def test_view_gives_response_status_code_302_simple_User(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_view_gives_response_status_code_200(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # TODO-не вдається отримати self.parent_id для перевірки
    @skip
    def test_view_gives_success_url(self):
        dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret')
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(dummy_user, 'Can add folder')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view.as_view()
        view = setup_view(self.cls_view, request, pk=1)
        v = view()
        response = v.dispatch(request, *view.args, **view.kwargs)
        print(v.__dict__)
        s = v.get_success_url()
        print(s)
        # view().dispatch(request, pk=1)
        # self.assertEqual(view.get_success_url(), "1")
        # self.assertEqual(view.parent_id, 1)


        # request = RequestFactory().get('/fake-path')
        # view = HelloView(template_name='hello.html')
        # view = setup_view(view, request, name='bob')
        # response = view.dispatch(view.request, *view.args, **view.kwargs)