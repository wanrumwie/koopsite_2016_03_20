from django.test import TestCase
from flats.models import Flat
from koopsite.functions import round_up_division, AllFieldsMixin


class FunctionsTest(TestCase):

    def test_round_up_division(self):
        self.assertEqual(round_up_division(5, 5), 1)
        self.assertEqual(round_up_division(101, 100), 2)
        self.assertEqual(round_up_division(200, 100), 2)
        self.assertEqual(round_up_division(100.001, 100), 2)
        self.assertEqual(round_up_division(100.001, 100.001), 1)


# @skip
class AllFieldsMixinTest(TestCase):
    # Тестуємо клас, базовий для AllFieldsView і AllRecordsAllFieldsView

    def test_all_fields_view_attributes(self):
        cls = AllFieldsMixin
        self.assertIsNone(cls.model)
        self.assertEqual(cls.fields, ())
        self.assertEqual(cls.exclude, ('id',))

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



