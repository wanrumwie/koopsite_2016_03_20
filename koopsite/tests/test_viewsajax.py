import json
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.test import TestCase
from functional_tests_koopsite.ft_base import DummyUser
from koopsite.functions import parseClientRequest, get_or_none
from koopsite.viewsajax import ajaxSelRowIndexToSession, \
                        ajaxStartRowIndexFromSession, BrowseTableArray


class TestajaxSelRowIndexToSession(TestCase):

    def test_function(self):
        json_s = '{"browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        request = self.client.request()
        request.POST = {'client_request': json_s}
        request.session = {}
        response = ajaxSelRowIndexToSession(request)
        expected = {'Selections': {'folders_contents': {'1': {'model': None, 'id': None, 'selRowIndex': '0'}}}}
        self.assertEqual(request.session, expected)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b'{"server_response": {"id": null, "selRowIndex": "0", "model": null}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_empty_response(self):
        request = self.client.request()
        request.POST = {}
        request.session = {}
        response = ajaxSelRowIndexToSession(request)
        self.assertEqual(request.session, {})
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)


class TestajaxStartRowIndexFromSession(TestCase):

    def test_function_return_HttpResponse(self):
        json_s = '{"browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        request = self.client.request()
        request.POST = {'client_request': json_s}
        request.session = {'Selections': {'folders_contents': {'1': {'model': None, 'id': None, 'selRowIndex': '0'}}}}
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b'{"server_response": {"id": null, "selRowIndex": "0", "model": null}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_HttpResponse_2(self):
        json_s = '{"browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        request = self.client.request()
        request.POST = {'client_request': json_s}
        expected = {'sendMail': None, 'id': None, 'name': None, 'browTabName': 'folders_contents', 'parent_id': '1', 'selRowIndex': '0', 'model': None}
        self.assertEqual(parseClientRequest(request.POST), expected)
        request.session = {
                   'Selections':
                        {"folders_contents":
                             {"1":
                                 {'model'       : "folder",
                                  'id'          : "1",
                                  'selRowIndex' : "2",
                                 },
                             },
                        },
                   }
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected = [b'{"server_response": {"id": "1", "selRowIndex": "2", "model": "folder"}}']
        self.assertEqual(json.loads(response._container[0].decode()) , json.loads(expected[0].decode()))
        expected = {'content-type': ('Content-Type', 'application/json')}
        self.assertEqual(response._headers, expected)

    def test_function_return_empty_response(self):
        request = self.client.request()
        request.POST = {}
        response = ajaxStartRowIndexFromSession(request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response._container, [b''])
        expected = {'content-type': ('Content-Type', 'text/html; charset=utf-8')}
        self.assertEqual(response._headers, expected)


class BrowseTableArrayTest(TestCase):

    def setUp(self):
        DummyUser().create_dummy_user('fred', id=1)
        DummyUser().create_dummy_user('john', id=2)
        self.bta_cls = BrowseTableArray

    def test_get_qs_array(self):
        qs = User.objects.all()
        expected = {0: {0: {'id': '1', 'model': 'user', 'name': 'fred'}}, 1: {0: {'id': '2', 'model': 'user', 'name': 'john'}}}
        arr = self.bta_cls().get_qs_array(qs)
        self.assertEqual(arr, expected)

    def test_get_qs_array_2(self):
        qs = User.objects.all()
        sel_model_id = {'id': '2', 'model': 'user', 'name': 'john'}
        expected = {0: {0: {'id': '1', 'model': 'user', 'name': 'fred'}}, 1: {0: {'id': '2', 'model': 'user', 'name': 'john'}}}
        arr, sel_index = self.bta_cls().get_qs_array(qs, sel_model_id=sel_model_id)
        self.assertEqual(arr, expected)
        self.assertEqual(sel_index, 1)
        sel_model_id = {'id': '3', 'model': 'user', 'name': 'john'}
        arr, sel_index = self.bta_cls().get_qs_array(qs, sel_model_id=sel_model_id)
        self.assertEqual(arr, expected)
        self.assertEqual(sel_index, 0)

    def test_get_table_headers(self):
        expected = {0:'', 1:'Name'}
        cap = self.bta_cls().get_table_headers()
        self.assertEqual(cap, expected)

    def test_get_row(self):
        user = get_or_none(User, id=1)
        expected = {0: {'id': '1', 'model': 'user', 'name': 'fred'}}
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

    def test_get_cell(self):
        user = get_or_none(User, id=1)
        expected = {'id': '1', 'model': 'user', 'name': 'fred'}
        row = self.bta_cls().get_cell(user, 0)
        self.assertEqual(row, expected)

    def test_get_cell_99(self):
        user = get_or_none(User, id=1)
        expected = None
        row = self.bta_cls().get_cell(user, 99)
        self.assertEqual(row, expected)

    def test_get_cell_changes(self):
        old = {
                0: {'name': 'fred', 'id': '1', 'model': 'user'},
                1: 'alfa',
                2: 250,
                }
        new = old.copy()
        expected = {0: {'name': 'fred', 'id': '1', 'model': 'user'},}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

        new = old.copy()
        new[1] = 'beta'
        expected = {0: {'name': 'fred', 'id': '1', 'model': 'user'}, 1: 'beta'}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

        new = old.copy()
        new[0] = {'name': 'paul', 'id': '1', 'model': 'user'}
        new[1] = 'beta'
        expected = {0: {'name': 'paul', 'id': '1', 'model': 'user'}, 1: 'beta'}
        changes = self.bta_cls().get_cell_changes(old, new)
        self.assertEqual(changes, expected)

    def test_get_supplement_data(self):
        user = get_or_none(User, id=1)
        expected = {}
        data = self.bta_cls().get_supplement_data(user)
        self.assertEqual(data, expected)

