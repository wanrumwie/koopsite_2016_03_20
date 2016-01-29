from copy import deepcopy
import inspect
import json
import types
from unittest.case import skip, skipIf
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import resolve
from django.http.response import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from flats.tests.test_base import DummyFlat
from functional_tests_koopsite.ft_base import DummyUser
from koopsite.functions import get_or_none, dict_print, parseClientRequest
from koopsite.models import UserProfile
from koopsite.settings import LOGIN_URL, SKIP_TEST
from koopsite.tests.test_views import setup_view
from koopsite.tests.test_viewsajax import DummyAjaxRequest, server_response_decrypt
from koopsite.viewsajax import msgType
from koopsite.viewsajaxuser import UsersTableArray, UsersTable, AjaxAccountView, AjaxRecognizeAccount


@skipIf(SKIP_TEST, "пропущено для економії часу")
class UsersTableArrayTest(TestCase):

    def setUp(self):
        user = DummyUser().create_dummy_user('fred', id=1)
        flat = DummyFlat().create_dummy_flat(id=1, flat_No='55')
        DummyUser().create_dummy_profile(user, flat=flat)
        user.first_name = 'Fred'
        user.last_name  = 'Aster'
        user.email      = 'user@gmail.com'
        user.save()
        DummyUser().create_dummy_user('john', id=2)
        self.bta_cls = UsersTableArray

    def test_get_table_headers(self):
        expected = {0: '', 1: 'Логін', 2: 'Користувач', 3: 'Кв.', 4: 'e-mail', 5: 'Дата ств.', 6: 'Підтв.', 7: 'Актив.', 8: 'Чл.кооп.'}
        cap = self.bta_cls().get_table_headers()
        self.assertEqual(cap, expected)

    def test_get_row(self):
        user = get_or_none(User, id=1)
        expected = {
            0: {'model': 'user', 'name': 'fred', 'id': '1'},
            1: 'fred',
            2: 'Aster Fred',
            3: '55',
            4: 'user@gmail.com',
            5: user.date_joined,
            6: None,
            7: True,
            8: False,
            }
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_row_2(self):
        user = get_or_none(User, id=3)
        expected = None
        row = self.bta_cls().get_row(user)
        self.assertEqual(row, expected)

    def test_get_model_id_name(self):
        user = get_or_none(User, id=1)
        expected = {'id': '1', 'model': 'user', 'name': 'fred'}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_model_id_name_2(self):
        user = get_or_none(User, id=3)
        expected = {}
        m_id_n = self.bta_cls().get_model_id_name(user)
        self.assertEqual(m_id_n, expected)

    def test_get_supplement_data(self):
        user = get_or_none(User, id=1)
        expected = {'iconPath': {
                            8: '/static/admin/img/icon-no.gif',
                            6: '/static/admin/img/icon-unknown.gif',
                            7: '/static/admin/img/icon-yes.gif',
                            }}
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)

    def test_get_supplement_data_2(self):
        user = get_or_none(User, id=3)
        expected = None
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)


@skipIf(SKIP_TEST, "пропущено для економії часу")
class UsersTableTest(TestCase):

    def setUp(self):
        self.cls_view = UsersTable
        self.path = '/adm/users/table/'
        self.template = 'koop_adm_users_table.html'
        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='staff')
        self.john   = DummyUser().create_dummy_user(username='john', password='secret')
        self.paul   = DummyUser().create_dummy_user(username='paul')
        self.george = DummyUser().create_dummy_user(username='george')
        self.ringo  = DummyUser().create_dummy_user(username='ringo', password='secret')
        DummyUser().add_dummy_group(self.john  , 'members')
        DummyUser().add_dummy_group(self.john  , 'staff')
        DummyUser().add_dummy_group(self.paul  , 'members')
        DummyUser().add_dummy_group(self.george, 'staff')
        DummyUser().add_dummy_permission(self.john, 'activate_account')
        self.john.is_staff = True
        self.john.save()
        self.dummy_user = AnonymousUser()


    def test_view_model_and_attributes(self):
        view = self.cls_view()
        self.assertEqual(view.model      , User)

    def test_url_resolves_to_proper_view(self):
        found = resolve(self.path)
        self.assertEqual(found.func.__name__, self.cls_view.__name__) #

    def test_view_renders_proper_template(self):
        self.client.login(username='john', password='secret')
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)

    def test_view_gives_response_status_code_302_AnonymousUser(self):
        request = RequestFactory().get(self.path)
        request.user = AnonymousUser()
        view = self.cls_view
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_302_user_w_o_permission(self):
        self.client.login(username='ringo', password='secret')
        request = RequestFactory().get(self.path)
        request.user = self.ringo
        view = self.cls_view
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_view_gives_response_status_code_200_setup(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_for_anonymous_user(self):

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        expected = [self.john, self.paul, self.ringo]
        self.assertEqual(view.get_queryset(), expected)

    def test_get_queryset_for_staff_user(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        qs = view.get_queryset()
        self.assertEqual(qs[0], self.george)
        self.assertEqual(qs[1], self.john)
        self.assertEqual(qs[2], self.paul)
        self.assertEqual(qs[3], self.ringo)

    def test_get_context_data(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        response = view.dispatch(view.request, *view.args, **view.kwargs)
        context = view.get_context_data(**kwargs)
        self.assertEqual(context['arr'            ], {0: {0: {'id': '3', 'model': 'user', 'name': 'george'}, 1: 'george', 2: '', 3: '', 4: '', 5: self.george.date_joined, 6: '', 7: True, 8: False}, 1: {0: {'id': '1', 'model': 'user', 'name': 'john'}, 1: 'john', 2: '', 3: '', 4: '', 5: self.john.date_joined, 6: '', 7: True, 8: True}, 2: {0: {'id': '2', 'model': 'user', 'name': 'paul'}, 1: 'paul', 2: '', 3: '', 4: '', 5: self.paul.date_joined, 6: '', 7: True, 8: True}, 3: {0: {'id': '4', 'model': 'user', 'name': 'ringo'}, 1: 'ringo', 2: '', 3: '', 4: '', 5: self.ringo.date_joined, 6: '', 7: True, 8: False}})
        self.assertEqual(context['browTabName'    ], "users_table")
        self.assertEqual(context['cap'            ], {0: '', 1: 'Логін', 2: 'Користувач', 3: 'Кв.', 4: 'e-mail', 5: 'Дата ств.', 6: 'Підтв.', 7: 'Актив.', 8: 'Чл.кооп.'})
        self.assertEqual(context['selElementID'   ], None)
        self.assertEqual(context['selElementModel'], None)
        self.assertEqual(context['selRowIndex'    ], 0)

        j_arr = deepcopy(context['arr'])   # arr - змінюваний об'єкт!
        for i in j_arr:
            if j_arr[i][5]: j_arr[i][5] = j_arr[i][5].isoformat()
        json_arr = json.dumps(j_arr)
        self.assertEqual(context['json_arr'       ], json_arr)

        self.assertEqual(request.session['Selections'], {'users_table': {'': {'model': None, 'id': None, 'selRowIndex': 0}}})


@skipIf(SKIP_TEST, "пропущено для економії часу")
class AjaxAccountViewTest(TestCase):

    def setUp(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        self.cls_view = AjaxAccountView
        # self.path = '/adm/users/table/'
        # self.template = 'koop_adm_users_table.html'

        self.msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )
        self.no_request_template = 'koop_adm_users_table.html'
        self.sendMail = False

        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='staff')
        self.john   = DummyUser().create_dummy_user(username='john', password='secret')
        self.paul   = DummyUser().create_dummy_user(username='paul')
        self.george = DummyUser().create_dummy_user(username='george')
        self.ringo  = DummyUser().create_dummy_user(username='ringo', password='secret')
        DummyUser().add_dummy_group(self.john  , 'members')
        DummyUser().add_dummy_group(self.john  , 'staff')
        DummyUser().add_dummy_group(self.paul  , 'members')
        DummyUser().add_dummy_group(self.george, 'staff')
        DummyUser().add_dummy_permission(self.john, 'activate_account')
        DummyUser().create_dummy_profile(self.john)
        self.john.is_staff = True
        self.john.save()
        self.dummy_user = AnonymousUser()


    def test_view_model_and_attributes(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        self.assertEqual(view.msg                , self.msg                )
        self.assertEqual(view.no_request_template, self.no_request_template)
        self.assertEqual(view.sendMail           , self.sendMail           )


    def test_get_request_data(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
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
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, self.john)
        self.assertEqual(profile, self.john.userprofile)


    def test_get_request_data_2_no_profile(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'2',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, self.paul)
        self.assertEqual(profile, None)

    def test_get_request_data_3_no_user(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)


    def test_get_request_data_4_no_model(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'users_table',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)


    def test_get_request_data_4_model_mismatch_table_name(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'folders_contents',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)


    def test_get_request_data_5_no_table_name(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)


    def test_get_request_data_6_unknown_table_name(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view
        kwargs = {
                    'browTabName' :'FOLDER',
                    'parent_id'   :"",
                    'sendMail'    :"",
                    'selRowIndex' :'0',
                    'model'       :'user',
                    'id'          :'99',
                    'name'        :'paul',
                }
        ajax_data = DummyAjaxRequest(**kwargs).ajax_data()
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}
        user, profile = view().get_request_data(request)
        # Чи метод повертає правильні записи?
        self.assertEqual(user, None)
        self.assertEqual(profile, None)


    """
    Метод processing треба переозначити у дочірньому класі.
    Тут наводиться приклад тесту.
    """

    def test_processing_no_changes_made(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        user0 = self.john
        prof0 = user0.userprofile
        prof0.is_recognized = True
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт вже підтверджений!")


    def test_processing_changes_made(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        user0 = self.john
        prof0 = user0.userprofile
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=self.john.id)
        prof_db = get_or_none(UserProfile, user=self.john)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(prof_db.is_recognized, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт підтверджено!")
        # TODO-2016 01 29 додати перевірку self.send_e_mail(user, e_msg_body)


    def test_handler(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
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
        request = self.client.request()
        request.POST = ajax_data
        request.session = {}

        response = view.handler(request)

        d = server_response_decrypt(response._container)
        dict_print(d, 'response._container', '='*20)

        # Чи ф-ція повертає правильний response?

        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'}, '6': True}
        expected_message    = "Акаунт підтверджено!"
        expected_supplement = {'iconPath': {'8': '/static/admin/img/icon-yes.gif', '7': '/static/admin/img/icon-yes.gif', '6': '/static/admin/img/icon-yes.gif'}}
        expected_title      = "john"
        expected_type       = "Change"

        self.assertEqual(d['changes'   ], expected_changes   )
        self.assertEqual(d['message'   ], expected_message   )
        self.assertEqual(d['supplement'], expected_supplement)
        self.assertEqual(d['title'     ], expected_title     )
        self.assertEqual(d['type'      ], expected_type      )

        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_handler_return_empty_response_if_no_client_request(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.handler(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)

    def test_dispatch(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()

        request = self.client.request()
        request.POST = {}
        response = view.dispatch(request)
        expected_response = view.handler(request)
        self.assertEqual(response.__dict__, expected_response.__dict__)


class AjaxRecognizeAccountTest(TestCase):

    def setUp(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        self.cls_view = AjaxRecognizeAccount
        self.path = '/adm/users/ajax-recognize-account'

        self.msg = types.SimpleNamespace(title   = "",
                                        type    = "",
                                        message = "",
                                        )
        self.no_request_template = 'koop_adm_users_table.html'
        self.sendMail = False

        DummyUser().create_dummy_group(group_name='members')
        DummyUser().create_dummy_group(group_name='staff')
        self.john   = DummyUser().create_dummy_user(username='john', password='secret')
        self.paul   = DummyUser().create_dummy_user(username='paul')
        self.george = DummyUser().create_dummy_user(username='george')
        self.ringo  = DummyUser().create_dummy_user(username='ringo', password='secret')
        DummyUser().add_dummy_group(self.john  , 'members')
        DummyUser().add_dummy_group(self.john  , 'staff')
        DummyUser().add_dummy_group(self.paul  , 'members')
        DummyUser().add_dummy_group(self.george, 'staff')
        DummyUser().add_dummy_permission(self.john, 'activate_account')
        DummyUser().create_dummy_profile(self.john)
        self.john.is_staff = True
        self.john.save()
        self.dummy_user = AnonymousUser()

    def test_processing_no_changes_made(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        user0 = self.john
        prof0 = user0.userprofile
        prof0.is_recognized = True
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        self.assertEqual(user, user0)
        self.assertEqual(msg.title  , user0.username)
        self.assertEqual(msg.type   , msgType.NoChange)
        self.assertEqual(msg.message, "Акаунт раніше вже був підтверджений!")


    def test_processing_changes_made(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
        view = self.cls_view()
        user0 = self.john
        prof0 = user0.userprofile
        user, msg = view.processing(user0, prof0, view.msg)
        # Витягаємо з бази щойно збережені записи і перевіряємо
        user_db = get_or_none(User, id=self.john.id)
        prof_db = get_or_none(UserProfile, user=self.john)
        self.assertEqual(user.id, user_db.id)
        self.assertEqual(prof_db.is_recognized, True)
        self.assertEqual(msg.title  , user_db.username)
        self.assertEqual(msg.type   , msgType.Change)
        self.assertEqual(msg.message, "Акаунт підтверджено!")
        # TODO-2016 01 29 додати перевірку self.send_e_mail(user, e_msg_body)

    def test_dispatch(self):
        print('started: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))
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

    def test_get_context_data(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        response = view.as_view()(request, **kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)

        d = server_response_decrypt(response._container)
        dict_print(d, 'response._container', '='*20)

        # Чи ф-ція повертає правильний response?

        expected_changes    = {'0': {'id': '1', 'name': 'john', 'model': 'user'}, '6': True}
        expected_message    = "Акаунт підтверджено!"
        expected_supplement = {'iconPath': {'8': '/static/admin/img/icon-yes.gif', '7': '/static/admin/img/icon-yes.gif', '6': '/static/admin/img/icon-yes.gif'}}
        expected_title      = "john"
        expected_type       = "Change"

        self.assertEqual(d['changes'   ], expected_changes   )
        self.assertEqual(d['message'   ], expected_message   )
        self.assertEqual(d['supplement'], expected_supplement)
        self.assertEqual(d['title'     ], expected_title     )
        self.assertEqual(d['type'      ], expected_type      )

        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

# TODO-2016 01 29 прибрати зайве з AjaxRecognizeAccountTest(TestCase) і на його основі зробити тести для всіх інших класів Ajax...


    @skip
    def test_view_gives_response_status_code_200(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        response = view.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    @skip
    def test_view_gives_response_status_code_200_setup(self):
        self.client.login(username='john', password='secret')
        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 200)

    @skip
    def test_get_queryset_for_anonymous_user(self):

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.dummy_user
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        expected = [self.john, self.paul, self.ringo]
        self.assertEqual(view.get_queryset(), expected)

    @skip
    def test_get_queryset_for_staff_user(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        qs = view.get_queryset()
        self.assertEqual(qs[0], self.george)
        self.assertEqual(qs[1], self.john)
        self.assertEqual(qs[2], self.paul)
        self.assertEqual(qs[3], self.ringo)

    @skip
    def test_get_context_data(self):
        self.client.login(username='john', password='secret')

        view = self.cls_view()
        request = RequestFactory().get(self.path)
        request.user = self.john
        request.session = {}
        kwargs = {}
        view = setup_view(view, request, **kwargs)

        response = view.dispatch(view.request, *view.args, **view.kwargs)
        context = view.get_context_data(**kwargs)
        self.assertEqual(context['arr'            ], {0: {0: {'id': '3', 'model': 'user', 'name': 'george'}, 1: 'george', 2: '', 3: '', 4: '', 5: self.george.date_joined, 6: '', 7: True, 8: False}, 1: {0: {'id': '1', 'model': 'user', 'name': 'john'}, 1: 'john', 2: '', 3: '', 4: '', 5: self.john.date_joined, 6: '', 7: True, 8: True}, 2: {0: {'id': '2', 'model': 'user', 'name': 'paul'}, 1: 'paul', 2: '', 3: '', 4: '', 5: self.paul.date_joined, 6: '', 7: True, 8: True}, 3: {0: {'id': '4', 'model': 'user', 'name': 'ringo'}, 1: 'ringo', 2: '', 3: '', 4: '', 5: self.ringo.date_joined, 6: '', 7: True, 8: False}})
        self.assertEqual(context['browTabName'    ], "users_table")
        self.assertEqual(context['cap'            ], {0: '', 1: 'Логін', 2: 'Користувач', 3: 'Кв.', 4: 'e-mail', 5: 'Дата ств.', 6: 'Підтв.', 7: 'Актив.', 8: 'Чл.кооп.'})
        self.assertEqual(context['selElementID'   ], None)
        self.assertEqual(context['selElementModel'], None)
        self.assertEqual(context['selRowIndex'    ], 0)

        j_arr = deepcopy(context['arr'])   # arr - змінюваний об'єкт!
        for i in j_arr:
            if j_arr[i][5]: j_arr[i][5] = j_arr[i][5].isoformat()
        json_arr = json.dumps(j_arr)
        self.assertEqual(context['json_arr'       ], json_arr)

        self.assertEqual(request.session['Selections'], {'users_table': {'': {'model': None, 'id': None, 'selRowIndex': 0}}})

