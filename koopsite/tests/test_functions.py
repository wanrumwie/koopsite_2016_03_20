import types
from unittest.case import skip
from django.contrib.auth.models import User
from django.test import TestCase
from flats.models import Flat
from folders.models import Folder
from koopsite.functions import round_up_division, AllFieldsMixin, get_namespace_from_dict, get_iconPathForFolder, \
    get_iconPathByFileExt, fileNameCheckInsert, scale_height, scale_width, getSelections, getSelElementFromSession, \
    setSelElementToSession, parseClientRequest, parseXHRClientRequest


class FunctionsTest(TestCase):

    def test_round_up_division(self):
        self.assertEqual(round_up_division(5, 5), 1)
        self.assertEqual(round_up_division(101, 100), 2)
        self.assertEqual(round_up_division(200, 100), 2)
        self.assertEqual(round_up_division(100.001, 100), 2)
        self.assertEqual(round_up_division(100.001, 100.001), 1)

    def test_get_iconPathForFolder(self):
        self.assertEqual(get_iconPathForFolder(True), 'img/open_folder.png')
        self.assertEqual(get_iconPathForFolder(False), 'img/folder.png')

    def test_get_iconPathByFileExt(self):
        self.assertEqual(get_iconPathByFileExt(""), "img/file-icons/32px/_page.png")
        self.assertEqual(get_iconPathByFileExt(".doc"), 'img/file-icons/32px/doc.png')


class FileNameCheckInsertTest(TestCase):

    def setUp(self):
        self.fileNameList = ['alfa.txt', 'beta.txt', 'beta (1).txt',
                             'gama.txt', 'gama (1).txt', 'gama (2).txt']

    def test_fileNameCheckInsert_1(self):
        fileName = 'delta.txt'
        expected = 'delta.txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_2(self):
        fileName = 'alfa.txt'
        expected = 'alfa (1).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_3(self):
        fileName = 'beta.txt'
        expected = 'beta (2).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)

    def test_fileNameCheckInsert_4(self):
        fileName = 'gama.txt'
        expected = 'gama (3).txt'
        self.assertEqual(fileNameCheckInsert(fileName, self.fileNameList), expected)


class Scale_height_width_Test(TestCase):

    def test_scale_width(self):
        self.assertEqual(scale_width(100, 100, 1000), (100, 100))
        self.assertEqual(scale_width(100, 100,    0), (  0,   0))
        self.assertEqual(scale_width(  0, 100,    0), (  0,   0))
        self.assertEqual(scale_width(100, 100,   30), ( 30,  30))

    def test_scale_height(self):
        self.assertEqual(scale_height(100, 100, 1000), (100, 100))
        self.assertEqual(scale_height(100, 100,    0), (  0,   0))
        self.assertEqual(scale_height(100,   0,    0), (  0,   0))
        self.assertEqual(scale_height(100, 100,   30), ( 30,  30))



class GetSelectionsTest(TestCase):

    def setUp(self):
        self.session = {}

    def test_getSelections(self):
        expected = {'foldertab':
                         {'1':
                             {'model'       : Folder,
                              'id'          : id,
                              'selRowIndex' : 55,
                             },
                         },
                    }
        self.session['Selections'] = expected
        self.assertEqual(getSelections(self.session), expected)

    def test_getSelections_2(self):
        self.session['Selections'] = None
        self.assertEqual(getSelections(self.session), {})

    def test_getSelections_3(self):
        self.session['q'] = 'a'
        self.assertEqual(getSelections(self.session), {})

    def test_getSelections_4(self):
        self.session['Selections'] = [1,]
        self.assertEqual(getSelections(self.session), {})

# @skip
class GetSelElementFromSessionTest(TestCase):

    def setUp(self):
        self.session = {}
        self.session['Selections'] = {'foldertab':
                                         {'1':
                                             {'model'       : Folder,
                                              'id'          : 12,
                                              'selRowIndex' : 55,
                                             },
                                         },
                                    }

    def test_selElementFromSessionTest(self):
        expected = {'model'       : Folder,
                    'id'          : 12,
                    'selRowIndex' : 55,
                    }
        b = 'foldertab'
        p = 1
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest2(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'usertab'
        p = 1
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest3(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'foldertab'
        p = 2
        self.assertEqual(getSelElementFromSession(self.session, b, p), expected)

    def test_selElementFromSessionTest4(self):
        expected = {'model'       : None,
                    'id'          : None,
                    'selRowIndex' : None,
                    }
        b = 'foldertab'
        self.assertEqual(getSelElementFromSession(self.session, b), expected)

class SetSelElementToSessionTest(TestCase):

    def setUp(self):
        self.session = {}

    def test_selElementToSessionTest(self):
        b = 'foldertab'
        p = 1
        s = {'model'      : Folder,
            'id'          : 12,
            'selRowIndex' : 55,
            }
        expected = {'foldertab':
                         {'1':
                             {'model'       : Folder,
                              'id'          : 12,
                              'selRowIndex' : 55,
                             },
                         },
                    }
        setSelElementToSession(self.session, b, p, s)
        self.assertEqual(self.session['Selections'], expected)
        p = '1'
        setSelElementToSession(self.session, b, p, s)
        self.assertEqual(self.session['Selections'], expected)

    def test_selElementToSessionTest_2(self):
        b = 'foldertab'
        p = 1
        expected = {'foldertab':
                         {'1':
                             {'model'       : None,
                              'id'          : None,
                              'selRowIndex' : None,
                             },
                         },
                    }
        setSelElementToSession(self.session, b, p)
        self.assertEqual(self.session['Selections'], expected)
        # TODO-нагадати собі, для чого зберігати в сесії дані з id=""?
        # setSelElementToSession(self.session, b)
        # self.assertEqual(self.session['Selections'], expected)

class ParseClientRequestTest(TestCase):

    def test_parseClientRequest(self):
        json_s = '{"browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        requestPOST = {'client_request': json_s}
        expected = {'sendMail': None, 'id': None, 'name': None, 'browTabName': 'folders_contents', 'parent_id': '1', 'selRowIndex': '0', 'model': None}
        self.assertEqual(parseClientRequest(requestPOST), expected)

    def test_parseClientRequest_can_expand_d(self):
        json_s = '{"alfa":"beta","browTabName":"folders_contents","parent_id":"1","selRowIndex":"0"}'
        requestPOST = {'client_request': json_s}
        expected = {'alfa': 'beta', 'sendMail': None, 'id': None, 'name': None, 'browTabName': 'folders_contents', 'parent_id': '1', 'selRowIndex': '0', 'model': None}
        self.assertEqual(parseClientRequest(requestPOST), expected)


class ParseXHRClientRequestTest(TestCase):

    def test_parseXHRClientRequest(self):
        # для тесту взято дані, роздруковані в ході виконання report download
        requestMETA = {'PYTHONIOENCODING': 'UTF-8', 'HTTP_X_CLIENT_REQUEST': '%7B%22browTabName%22%3A%22folders_contents%22%2C%22parent_id%22%3A%227%22%2C%22selRowIndex%22%3A%222%22%2C%22model%22%3A%22report%22%2C%22id%22%3A%22130%22%2C%22name%22%3A%22%D0%92%D1%96%D0%B4%D1%80%D1%8F%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.tif%22%7D', }
        expected = {'model': 'report', 'browTabName': 'folders_contents', 'selRowIndex': '2', 'id': '130', 'parent_id': '7', 'name': 'Відрядження.tif'}
        self.assertEqual(parseXHRClientRequest(requestMETA), expected)


class Get_namespace_from_dictTest(TestCase):
    def setUp(self):
        self.ns = types.SimpleNamespace(
                                        a   = None,
                                        b   = None,
                                        c   = None,
                                        )

    def test_get_namespace_from_dict_1(self):
        d = {'a':1, 'b':2}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_2(self):
        d = {'a':1, 'b':2, 'd':4}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_3(self):
        d = {'a':1, 'b':2}
        expected = types.SimpleNamespace(a=1, b=2, c= None)
        ns = get_namespace_from_dict(d, self.ns, True)
        self.assertEqual(ns, expected)

    def test_get_namespace_from_dict_4(self):
        d = {'a':1, 'b':2, 'd':4}
        expected = types.SimpleNamespace(a=1, b=2, c= None, d= 4)
        ns = get_namespace_from_dict(d, self.ns, True)
        self.assertEqual(ns, expected)


# @skip
class AllFieldsMixinTest(TestCase):
    # Тестуємо клас, базовий для AllFieldsView і AllRecordsAllFieldsView

    def test_attributes(self):
        cls = AllFieldsMixin
        self.assertIsNone(cls.model)
        self.assertEqual(cls.fields, ())
        self.assertEqual(cls.exclude, ())

    def test_val_repr(self):
        cls = AllFieldsMixin()
        self.assertEqual(cls.val_repr(5), 5)
        self.assertEqual(cls.val_repr(5.1), 5.1)
        self.assertEqual(cls.val_repr(5.12), 5.12)
        self.assertEqual(cls.val_repr(5.123), 5.12)
        self.assertEqual(cls.val_repr(5.126), 5.13)
        self.assertEqual(cls.val_repr(5.126, 1), 5.1)
        self.assertEqual(cls.val_repr(0), "")
        self.assertEqual(cls.val_repr("qwe"), "qwe")

    def test_get_field_keys_verbnames_gives_all_fields_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        cls.fields = ()
        cls.exclude = ('id',)
        key_list, verbname_list = cls.get_field_keys_verbnames()
        # Списки мають мати довжину == кількості полів у моделі Flat
        self.assertEqual(len(key_list), 23)
        self.assertEqual(len(verbname_list), 23)
        # id не входить до списку
        self.assertNotIn('id', key_list)
        # Вибіркова перевірка:
        self.assertEqual(key_list[0], "flat_No")
        self.assertEqual(verbname_list[0], "Квартира №")
        self.assertEqual(key_list[5], "room1_S")
        self.assertEqual(verbname_list[5], "кімната")
        self.assertEqual(key_list[22], "listing")
        self.assertEqual(verbname_list[22], "Список")

    def test_get_field_keys_verbnames_gives_some_fields_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        cls.fields = ("flat_No", "room1_S", "listing")
        cls.exclude = ('id',)
        key_list, verbname_list = cls.get_field_keys_verbnames()
        # Списки мають мати довжину == кількості полів у self.fields
        self.assertEqual(len(key_list), 3)
        self.assertEqual(len(verbname_list), 3)
        # id не входить до списку
        self.assertNotIn('id', key_list)
        # Вибіркова перевірка:
        self.assertEqual(key_list[0], "flat_No")
        self.assertEqual(verbname_list[0], "Квартира №")
        self.assertEqual(key_list[1], "room1_S")
        self.assertEqual(verbname_list[1], "кімната")
        self.assertEqual(key_list[2], "listing")
        self.assertEqual(verbname_list[2], "Список")

    def test_get_value_list_gives_proper_values_for_Flat(self):
        cls = AllFieldsMixin()
        cls.model = Flat
        flat = Flat(id=5, flat_No='5', floor_No=1, entrance_No=2)
        flat.save()
        key_list = ("flat_No", "floor_No", "entrance_No")
        value_list = cls.get_value_list(flat, key_list)
        # Списки мають мати довжину
        self.assertEqual(len(value_list), 3)
        # Перевірка значень:
        self.assertEqual(value_list[0], '5')
        self.assertEqual(value_list[1], 1)
        self.assertEqual(value_list[2], 2)

    def test_get_label_value_list_gives_list_of_tuples(self):
        cls = AllFieldsMixin()
        key_list = ("flat_No", "floor_No", "entrance_No")
        value_list = ('1', 2, 3)
        kv_list = cls.get_label_value_list(key_list, value_list)

        # Список має мати довжину:
        self.assertEqual(len(kv_list), 3)
        # Перевірка значень:
        self.assertEqual(kv_list[0], ("flat_No", '1'))
        self.assertEqual(kv_list[1], ("floor_No", 2))
        self.assertEqual(kv_list[2], ("entrance_No", 3))



