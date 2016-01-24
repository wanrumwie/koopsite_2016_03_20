import inspect
from datetime import timedelta
from unittest.case import skip
from django import forms
from django.contrib.auth.models import User, AnonymousUser, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import now
from flats.models import Flat
from flats.tests.test_base import DummyFlat
from koopsite.forms import UserRegistrationForm, ProfileRegistrationForm, Human_Check, UserPermsFullForm, \
    ProfilePermForm, UserPersonDataForm, ProfilePersonDataForm
from koopsite.functions import dict_print, has_group
from koopsite.models import UserProfile
from koopsite.settings import LOGIN_URL
from koopsite.tests.test_base import DummyUser
from koopsite.views import index, AllFieldsView, AllRecordsAllFieldsView, OneToOneBase, OneToOneCreate, \
    UserProfileCreate, UserProfilePersonDataUpdate, UserPermsFullUpdate


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


class OneToOneBaseTest(TestCase):

    def setUp(self):
        self.cls_view = OneToOneBase
        # self.path = '/folders/list/'
        # self.template = 'folders/folder_list.html'

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.render_variant, "as_table")
        self.assertEqual(view.form_one_name , 'form_one')
        self.assertEqual(view.form_two_name , 'form_two')
        self.assertEqual(view.finished      , False)
        self.assertEqual(view.rel_name      , '')
        self.assertEqual(view.oto_name      , '')
        self.assertEqual(view.capital_name  , '')
        self.assertEqual(view.FormOne       , forms.ModelForm)
        self.assertEqual(view.FormTwo       , forms.ModelForm)
        self.assertEqual(view.ModelTwo      , models.Model)
        self.assertEqual(view.ModelOne      , models.Model)
        self.assertEqual(view.one_fields    , None)
        self.assertEqual(view.two_fields    , None)
        self.assertEqual(view.one_img_fields, None)
        self.assertEqual(view.two_img_fields, None)

    def test_get_one(self):
        view = self.cls_view()
        view.ModelOne = User
        user = DummyUser().create_dummy_user(id=1)
        request = RequestFactory()
        kwargs = {'pk' : 1}
        one = view.get_one(request, **kwargs)
        self.assertEqual(one, user)

    def test_get_two(self):
        view = self.cls_view()
        view.ModelOne = User
        view.ModelTwo = UserProfile
        view.rel_name = 'userprofile'
        view.oto_name = 'user'
        user = DummyUser().create_dummy_user(id=1)
        profile = DummyUser().create_dummy_profile(user)
        two = view.get_two(user)
        self.assertEqual(two, profile)

    def test_get_two_if_except(self):
        view = self.cls_view()
        view.ModelOne = User
        view.ModelTwo = UserProfile
        view.rel_name = 'userprofile'
        view.oto_name = 'user'
        user = DummyUser().create_dummy_user(id=1)
        two = view.get_two(user)
        self.assertEqual(getattr(two, view.oto_name), user)

    def test_set_one_outform_fields(self):
        view = self.cls_view()
        user = DummyUser().create_dummy_user(id=1)
        with self.assertRaises(AssertionError):
            view.set_one_outform_fields(user)

    def test_set_two_outform_fields(self):
        view = self.cls_view()
        user = DummyUser().create_dummy_user(id=1)
        with self.assertRaises(AssertionError):
            view.set_two_outform_fields(user)

    """
    'username'
    'first_name'
    'last_name'
    'password'
    'email'
    'is_active'
    'is_staff'
    'date_joined'
    'last_login'
    'groups'
    'has_perm_member'
    'flat'
    'picture'
    'is_recognized'
    'human_check'
    """


class UserProfileCreateTest(TestCase):
    '''
    Цим тестом одночасно перевіряється OneToOneCreate
    '''

    def setUp(self):
        Human_Check.if_view_test = True
        self.cls_view = UserProfileCreate
        self.path = '/register/'
        self.template = 'koop_user_prof_create.html'
        self.dummy_user = AnonymousUser()

    def tearDown(self):
        Human_Check.if_view_test = False

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.render_variant, "as_table")
        self.assertEqual(view.form_one_name , 'form_one')
        self.assertEqual(view.form_two_name , 'form_two')
        self.assertEqual(view.finished      , False)
        self.assertEqual(view.rel_name      , 'userprofile')
        self.assertEqual(view.oto_name      , 'user')
        self.assertEqual(view.capital_name  , 'username')
        self.assertEqual(view.FormOne       , UserRegistrationForm)
        self.assertEqual(view.FormTwo       , ProfileRegistrationForm)
        self.assertEqual(view.ModelOne      , User)
        self.assertEqual(view.ModelTwo      , UserProfile)
        self.assertEqual(view.one_fields    , None)
        self.assertEqual(view.two_fields    , None)
        self.assertEqual(view.one_img_fields, None)
        self.assertEqual(view.two_img_fields, None)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        view = self.cls_view.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        response = view.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form id="one_two_form"', response._container[0], request)

    def test_post_success_for_minimum_needed_data(self):
        view = self.cls_view

        # Передаємо у форму значення:
        data = {
            'username'  : 'fred',
            'password'  : 'secret',
            'human_check' : 'abrakadabra'
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази щойно створений запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.is_active, False)
        self.assertNotEqual(user.password, None)
        self.assertNotEqual(user.password, 'secret')

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile.user, user)
        self.assertEqual(user.is_active, False)

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)


    def test_post_success_for_maximum_needed_data(self):
        view = self.cls_view

        # file = SimpleUploadedFile("file.txt", b"file_content")
        with open("example.jpg", "rb") as file:
            file_content = file.read()
        file = open("example.jpg", "rb")
        flat = DummyFlat().create_dummy_flat(id=1)

        # Передаємо у форму значення:
        data = {
            'username'  : 'fred',
            'password'  : 'secret',
            'first_name': 'Fred',
            'last_name' : 'Stone',
            'email'     : 'fred@gmail.com',
            'flat'      : '1',
            'picture'   : file,
            'human_check': 'abrakadabra'
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази щойно створений запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, 'Fred')
        self.assertEqual(user.last_name, 'Stone')
        self.assertEqual(user.email, 'fred@gmail.com')
        self.assertEqual(user.is_active, False)

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.flat, flat)
        self.assertEqual(profile.picture.file.read(), file_content)

        file.close()
        profile.picture.delete()

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)


    def unsuccess_for_invalid_data(self, data):
        view = self.cls_view

        # Передаємо у форму значення:
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази щойно створений запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user, None)

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile, None)

        # Переадресовано на ту ж сторінку з полями errors
        self.assertEqual(response.status_code, 200)


    def test_post_unsuccess_for_empty_username(self):
        data = {
            # 'username'  : 'fred',
            'password'  : 'secret',
            'human_check': 'abrakadabra'
            }
        self.unsuccess_for_invalid_data(data)

    def test_post_unsuccess_for_empty_password(self):
        data = {
            'username'  : 'fred',
            # 'password'  : 'secret',
            'email'     : 'fred@gmail.com',
            'human_check': 'abrakadabra'
            }
        self.unsuccess_for_invalid_data(data)

    def test_post_unsuccess_for_invalid_email(self):
        data = {
            'username'  : 'fred',
            'password'  : 'secret',
            'email'     : 'fred_gmail.com',
            'human_check': 'abrakadabra'
            }
        self.unsuccess_for_invalid_data(data)

    def test_post_unsuccess_for_invalid_human_check(self):
        Human_Check.if_view_test = False
        data = {
            'username'  : 'fred',
            'password'  : 'secret',
            # 'email'     : 'fred@gmail.com',
            'human_check': 'abrakadabra'
            }
        self.unsuccess_for_invalid_data(data)

    def test_post_unsuccess_for_invalid_picture(self):
        file = SimpleUploadedFile("file.txt", b"file_content")
        data = {
            'username'  : 'fred',
            'password'  : 'secret',
            'picture'    : file,
            'human_check': 'abrakadabra'
            }
        self.unsuccess_for_invalid_data(data)


class UserProfilePersonDataUpdateTest(TestCase):
    '''
    Цим тестом одночасно перевіряється OneToOneUpdate
    '''

    def setUp(self):
        Human_Check.if_view_test = True
        self.cls_view = UserProfilePersonDataUpdate
        self.path = '/adm/users/1/profile/update/'
        self.template = 'koop_adm_user_prof_update.html'
        self.dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret', id=1)
        self.client.login(username='fred', password='secret')
        DummyUser().add_dummy_permission(self.dummy_user, 'change_userprofile')

    def tearDown(self):
        Human_Check.if_view_test = False

    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.render_variant, "as_table")
        self.assertEqual(view.form_one_name , 'form_one')
        self.assertEqual(view.form_two_name , 'form_two')
        self.assertEqual(view.finished      , False)
        self.assertEqual(view.rel_name      , 'userprofile')
        self.assertEqual(view.oto_name      , 'user')
        self.assertEqual(view.capital_name  , 'username')
        self.assertEqual(view.FormOne       , UserPersonDataForm)
        self.assertEqual(view.FormTwo       , ProfilePersonDataForm)
        self.assertEqual(view.ModelOne      , User)
        self.assertEqual(view.ModelTwo      , UserProfile)
        self.assertEqual(view.one_fields    , None)
        self.assertEqual(view.two_fields    , None)
        self.assertEqual(view.one_img_fields, None)
        self.assertEqual(view.two_img_fields, None)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        dummy_user =  DummyUser().create_dummy_user(username='john', password='secret')
        self.client.login(username='john', password='secret')
        request = RequestFactory().get(self.path)
        request.user = dummy_user
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        view = self.cls_view

        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form id="one_two_form"', response._container[0], request)

    def test_post_success_for_maximum_needed_data(self):
        view = self.cls_view

        with open("example.jpg", "rb") as file:
            file_content = file.read()
        file = open("example.jpg", "rb")
        flat = DummyFlat().create_dummy_flat(id=1)

        # Передаємо у форму значення:
        data = {
            'first_name': 'Fred',
            'last_name' : 'Stone',
            'email'     : 'fred@gmail.com',
            'flat'      : '1',
            'picture'   : file,
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, 'Fred')
        self.assertEqual(user.last_name, 'Stone')
        self.assertEqual(user.email, 'fred@gmail.com')

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.flat, flat)
        self.assertEqual(profile.picture.file.read(), file_content)

        file.close()
        profile.picture.delete()

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)


    def test_post_success_for_no_profile_data(self):
        view = self.cls_view

        # Передаємо у форму значення:
        data = {
            'first_name': 'Fred',
            'last_name' : 'Stone',
            'email'     : 'fred@gmail.com',
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, 'Fred')
        self.assertEqual(user.last_name, 'Stone')
        self.assertEqual(user.email, 'fred@gmail.com')

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile.user, user)

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)


    def test_post_success_for_profile_already_created(self):
        view = self.cls_view

        DummyUser().create_dummy_profile(self.dummy_user)

        flat = DummyFlat().create_dummy_flat(id=1)

        # Передаємо у форму значення:
        data = {
            'first_name': 'Fred',
            'last_name' : 'Stone',
            'email'     : 'fred@gmail.com',
            'flat'      : '1',
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.last()
        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, 'Fred')
        self.assertEqual(user.last_name, 'Stone')
        self.assertEqual(user.email, 'fred@gmail.com')

        profile = view.ModelTwo.objects.last()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.flat, flat)

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)


    def test_post_unsuccess_for_invalid_email(self):
        view = self.cls_view
        data = {
            'email'     : 'fred_gmail.com',
            }

        # Передаємо у форму значення:
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.get(id=1)
        self.assertEqual(user.email, "")

        # Переадресовано на ту ж сторінку з полями errors
        self.assertEqual(response.status_code, 200)

    def test_post_unsuccess_for_invalid_picture(self):
        view = self.cls_view
        file = SimpleUploadedFile("file.txt", b"file_content")
        data = {
            'picture'    : file,
            }

        # Передаємо у форму значення:
        request = RequestFactory().post(self.path, data)
        request.user = self.dummy_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.get(id=1)
        with self.assertRaises(ObjectDoesNotExist):
            view.ModelTwo.objects.get(user=user)

        # Переадресовано на ту ж сторінку з полями errors
        self.assertEqual(response.status_code, 200)


class UserPermsFullUpdateTest(TestCase):
    '''
    Цим тестом одночасно перевіряється OneToOneUpdate
    '''

    def setUp(self):
        Human_Check.if_view_test = True
        self.cls_view = UserPermsFullUpdate
        self.path = '/adm/users/1/perms/update/'
        self.template = 'koop_adm_user_perm_update.html'

        self.dummy_user =  DummyUser().create_dummy_user(username='fred', password='secret', id=1)
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='street')
        DummyUser().add_dummy_group(self.dummy_user, 'members')
        self.dummy_prof = DummyUser().create_dummy_profile(self.dummy_user)

        self.login_user =  DummyUser().create_dummy_user(username='john', password='secret', id=2)
        self.client.login(username='john', password='secret')
        DummyUser().add_dummy_permission(self.login_user, 'change_permission')


    def tearDown(self):
        Human_Check.if_view_test = False

    def test_view_model_and_attributes(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        self.assertEqual(view.render_variant, "as_table")
        self.assertEqual(view.form_one_name , 'form_one')
        self.assertEqual(view.form_two_name , 'form_two')
        self.assertEqual(view.finished      , False)
        self.assertEqual(view.rel_name      , 'userprofile')
        self.assertEqual(view.oto_name      , 'user')
        self.assertEqual(view.capital_name  , 'username')
        self.assertEqual(view.FormOne       , UserPermsFullForm)
        self.assertEqual(view.FormTwo       , ProfilePermForm)
        self.assertEqual(view.ModelOne      , User)
        self.assertEqual(view.ModelTwo      , UserProfile)
        self.assertEqual(view.one_fields    , None)
        self.assertEqual(view.two_fields    , None)
        self.assertEqual(view.one_img_fields, None)
        self.assertEqual(view.two_img_fields, None)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        login_user =  DummyUser().create_dummy_user(username='ringo', password='secret')
        self.client.login(username='ringo', password='secret')
        request = RequestFactory().get(self.path)
        request.user = login_user
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        request = RequestFactory().get(self.path)
        request.user = self.login_user
        view = self.cls_view
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        view = self.cls_view

        request = RequestFactory().get(self.path)
        request.user = self.login_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form id="one_two_form"', response._container[0], request)

    def test_post_success_for_maximum_needed_data(self):
        view = self.cls_view

        flat = DummyFlat().create_dummy_flat(id=1)

        # Передаємо у форму значення
        # Слід вказати всі дані, в т.ч. і в полях readonly,
        # принаймні у тих, які проходять валідацію у формі:
        data = {
            # read only:
            'username'      : 'fred',
            'first_name'    : '',
            'last_name'     : '',
            'date_joined'   : '',
            'last_login'    : '',

            'is_active'     : True,
            'is_staff'      : True,
            'groups'        : '2',

            'is_recognized' : True,

            # read only:
            'flat'          : '1',
            }
        request = RequestFactory().post(self.path, data)
        request.user = self.login_user
        kwargs = {'pk': 1}
        response = view.as_view()(request, **kwargs)

        # Витягаємо з бази запис:
        user = view.ModelOne.objects.get(id=1)

        self.assertEqual(user.username, 'fred')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertAlmostEqual(user.date_joined, now(), delta=timedelta(minutes=1))
        self.assertEqual(user.last_login, None)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertTrue(has_group(user, 'street'))

        profile = view.ModelTwo.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.flat, flat)
        self.assertEqual(profile.is_recognized, True)

        # Переадресовано на ту ж сторінку з прапорцем finished = True
        self.assertEqual(response.status_code, 200)





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



