from copy import deepcopy
import inspect
import json
import types
from unittest.case import skip, skipIf
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.http.response import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from flats.tests.test_base import DummyFlat
from functional_tests_koopsite.ft_base import DummyUser
from koopsite.functions import get_or_none, dict_print, parseClientRequest, has_group
from koopsite.models import UserProfile
from koopsite.settings import LOGIN_URL, SKIP_TEST
from koopsite.tests.test_views import setup_view
from koopsite.tests.test_viewsajax import DummyAjaxRequest, server_response_decrypt
from koopsite.tests.test_viewsajaxuser import AjaxAccountTestBase
from koopsite.viewsajax import msgType
from koopsite.viewsajaxuser import UsersTableArray, UsersTable, AjaxAccountViewBase, AjaxRecognizeAccount, AjaxDenyAccount, \
    AjaxActivateAccount, AjaxDeactivateAccount, AjaxSetMemberAccount, AjaxDenyMemberAccount, AjaxDeleteAccount, \
    AjaxAllAccountsViewBase


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxAllAccountsViewTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxAllAccountsViewBase

    # def test_view_model_and_attributes(self):
    #     view = self.cls_view()

    def test__init__(self):
        view = self.cls_view()

        self.assertEqual(view.empty_msg, self.msg     )
        # self.assertEqual(view.group_msg, self.msg     )
        self.assertEqual(view.sendMail , self.sendMail)
        self.assertEqual(view.group_msg.title  ,"Активація групи акаунтів")
        self.assertEqual(view.group_msg.type   ,msgType.Group)
        self.assertEqual(view.group_msg.message,"")
        self.assertEqual(view.counter          , {
                                                "вже активні" : 0,
                                                "відхилені"   : 0,
                                                "активовано"  : 0,
                                                }
        )

    def test_init_counter(self):
        view = self.cls_view()
        view.init_counter()
        self.assertEqual(view.group_msg.title  ,"Активація групи акаунтів")
        self.assertEqual(view.group_msg.type   ,msgType.Group)
        self.assertEqual(view.group_msg.message,"")
        self.assertEqual(view.counter          , {
                                                "вже активні" : 0,
                                                "відхилені"   : 0,
                                                "активовано"  : 0,
                                                }
        )

    def get_elemSet(self, userSet):
        elemSet = []
        for user in userSet:
            elem = {
                    'model': 'user',
                    'id'   : user.id,
                    'name' : user.username,
                    }
            elemSet.append(elem)
        return elemSet

    def get_kwargs_for_ajax_data(self, elemSet):
        kwargs = {
                    'browTabName' : 'users_table',
                    'parent_id'   : "",
                    'sendMail'    : "",
                    'selRowIndex' : '0',
                    'elemSet'     : elemSet,
                }
        return kwargs

    def test_get_request_data_set(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_list = users_list
        self.assertEqual(users_set, expected_users_list)

    def test_get_request_data_2_no_users(self):
        view = self.cls_view
        users_list = []
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_list = []
        self.assertEqual(users_set, expected_users_list)

    def test_get_request_data_4_no_model(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['elemSet'][0]['model'] = ""
        dict_print(kwargs)
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = users_list[1:]
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_4_model_mismatch_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = 'folders_contents'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_5_no_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = ''
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)


    def test_get_request_data_6_unknown_table_name(self):
        view = self.cls_view
        users_list = [self.john, self.paul, self.george, self.ringo]
        elemSet = self.get_elemSet(users_list)
        kwargs = self.get_kwargs_for_ajax_data(elemSet)
        kwargs['browTabName'] = 'FOLDER'
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        users_set = view().get_request_data_set(request)
        # Чи метод повертає правильні записи?
        expected_users_set = None
        self.assertEqual(users_set, expected_users_set)

    """
    Метод processing треба переозначити у дочірньому класі.
    Тут наводиться приклад тесту.
    """
    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже активний!")
        self.assertEqual(view.counter["вже активні"], 1)

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не можна активувати!")
        self.assertEqual(view.counter["відхилені"], 1)

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")
        self.assertEqual(view.counter["активовано"], 1)

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.empty_msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")
        self.assertEqual(view.counter["активовано"], 1)


        # TODO-2016 02 01 додати перевірку self.send_e_mail(user, e_msg_body)

'''

    def test_handler(self):
        view = self.cls_view()
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт раніше вже був підтверджений!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}

        response = view.handler(request)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_handler_return_empty_response_if_no_client_request(self):
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_dispatch(self):
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)



@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxActivateAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxActivateAccount
        self.path = '/adm/users/ajax-activate-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже активний!")

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не можна активувати!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")

    def test_processing_changes_made_no_profile(self):
        view = self.cls_view()
        user0 = self.ringo
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(user_db.is_active, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт активовано!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже активний!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'3',
                    'name'        :'george',
                }
        self.paul.userprofile.is_recognized = False
        self.paul.userprofile.save()
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "george"
        expected_type       = "Change"
        expected_message    = "Акаунт активовано!"
        expected_changes    = {'0': {'id': '3', 'name': 'george', 'model': 'user'},
                               '7': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-no.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxSetMemberAccountTest(AjaxAccountTestBase):

    def setUp(self):
        super().setUp()
        self.cls_view = AjaxSetMemberAccount
        self.path = '/adm/users/ajax-set-member-account'

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__)

    def test_dispatch(self):
        view = self.cls_view()
        request = self.client.request()
        request.POST = {}
        request.user = self.john
        request.session = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_response_raise_exception_AnonymousUser(self):
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_view_response_raise_exception_user_w_o_permission(self):
        self.client.login(username='paul', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        request.session = {}
        kwargs = {}
        with self.assertRaises(PermissionDenied):
            view.as_view()(request, **kwargs)

    def test_processing_no_changes_made(self):
        view = self.cls_view()
        user0 = self.john
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже має ці права доступу!")

    def test_processing_error_account_is_denied(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        prof0.is_recognized = False
        prof0.save()
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.Error)
        self.assertEqual(msg.message, "Відхилений Акаунт не може отримати права доступу!")

    def test_processing_changes_made(self):
        view = self.cls_view()
        user0 = self.george
        prof0 = getattr(user0, 'userprofile', None)
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=user0.id)
        prof_db = get_or_none(UserProfile, user=user0)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(has_group(user_db, 'members'), True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Права доступу встановлено!")

    def test_view_response_container_data_No_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'1',
                    'name'        :'john',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "john"
        expected_type       = "NoChange"
        expected_message    = "Акаунт вже має ці права доступу!"
        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'},
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)

    def test_view_response_container_data_Make_changes(self):
        self.client.login(username='john', password='secret')
        # Дані для request
        kwargs = {  'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        # Очікувані дані з response
        expected_title      = "paul"
        expected_type       = "Change"
        expected_message    = "Права доступу встановлено!"
        expected_changes    = {'0': {'id': '2', 'name': 'paul', 'model': 'user'},
                               '8': True,
                               }
        expected_supplement = {'iconPath': {
                            '6': '/static/admin/img/icon-yes.gif',
                            '7': '/static/admin/img/icon-yes.gif',
                            '8': '/static/admin/img/icon-yes.gif',
                            }}
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.POST = ajax_data
        request.session = {}

        view = self.cls_view
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        self.check_view_response_container_data(response,
            expected_title, expected_type, expected_message,
            expected_changes, expected_supplement)


'''
