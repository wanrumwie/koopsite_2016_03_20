import inspect
from unittest.mock import Mock
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import redirect_to_login
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test.client import RequestFactory
from folders.tests.test_base import DummyFolder
from folders.views import reportDecorView
from koopsite.decorators import owner_or_permission_required, request_passes_test
from koopsite.settings import LOGIN_URL, SKIP_TEST
from koopsite.tests.test_base import DummyUser
from koopsite.tests.test_views import setup_view


class OwnerPermissionDecoratorTest(TestCase):

    def setUp(self):


        # Параметри, при яких декоратор пропускає до функції:
        user = Mock(name='user')
        user.has_perms = Mock()
        user.has_perms.return_value = True

        user2 = Mock(name='user2')
        user2.has_perms = Mock()
        user2.has_perms.return_value = True

        object = Mock(name='object')
        object.owner = user

        object2 = Mock(name='object2')
        object2.owner = 'xxx'

        model = {1: object, 2: object2}

        request = RequestFactory()
        request.build_absolute_uri = Mock()
        request.build_absolute_uri.return_value = "" # path
        request.get_full_path = Mock()
        request.get_full_path.return_value = "" # path
        request.user = user

        view_func = Mock()
        view_func.return_value = 'passed'

        test_func = Mock()
        test_func.return_value = True

        self.user = user
        self.user2 = user2
        self.object = object
        self.model = model
        self.request = request
        self.view_func = view_func
        self.test_func = test_func
        self.perm = 'can'

        # print(self.user)
        # print(self.object)
        # print(self.object.pk)
        # print(self.model)
        # print(self.model())
        # print(self.request)
        # print(self.request.user)
        # ob = getattr(model, 'pk')
        # print(ob)


    def test_request_passes_test_True(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        test_func = self.test_func
        view_func = self.view_func

        decorated = request_passes_test(test_func)

        self.assertEqual(test_func(0), True)
        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request), 'passed')
        self.assertEqual(decorated(view_func)(self.request, 's'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')

    def test_request_passes_test_False(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        test_func = self.test_func
        view_func = self.view_func

        test_func.return_value = False

        decorated = request_passes_test(test_func)

        self.assertEqual(test_func(0), False)
        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request)), HttpResponseRedirect)
        # Детальніше не перевіряю, оскільки весь код після
        #     return view_func(request, *args, **kwargs)
        # без змін взято з user_passes_test()


    def test_owner_or_permission_required_Owner_1_Permission_True(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        view_func = self.view_func

        decorated = owner_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')


    def test_owner_or_permission_required_Owner_1_Perm_False(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        view_func = self.view_func

        self.user.has_perms.return_value = False

        decorated = owner_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request, pk='2')), HttpResponseRedirect)


    def test_owner_or_permission_required_Owner_False_Perm_True(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        view_func = self.view_func

        self.request.user = self.user2

        decorated = owner_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='1'), 'passed')
        self.assertEqual(decorated(view_func)(self.request, pk='2'), 'passed')


    def test_owner_or_permission_required_Owner_False_Perm_False(self):
        print('started:=========================== %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

        view_func = self.view_func

        self.request.user = self.user2
        self.user2.has_perms.return_value = False

        decorated = owner_or_permission_required(self.model, self.perm)

        self.assertEqual(view_func(0), 'passed')
        self.assertEqual(type(decorated(view_func)(self.request, pk='1')), HttpResponseRedirect)
        self.assertEqual(type(decorated(view_func)(self.request, pk='2')), HttpResponseRedirect)


