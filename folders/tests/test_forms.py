from unittest.case import skip
from django.test import TestCase
from folders.forms import FolderForm
from folders.models import Folder
from folders.tests.test_base import DummyFolder
from koopsite.forms import EMPTY_FIELD_ERROR
from lists.forms import (
    ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR)
from lists.models import List, Item
from django import forms


class FolderFormTest(TestCase):

    def setUp(self):
        self.cls_form = FolderForm
        self.parent_folder = DummyFolder().create_dummy_root_folder()
        self.initial_data = {'parent': self.parent_folder}
        self.empty_data = {'parent': "", 'name': "", 'created_on': ""}

    def test_form_attributes(self):
        form = self.cls_form
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, Folder)
        self.assertEqual(form.Meta.fields, ('parent', 'name', 'created_on'))

    def test_form_renders_blank(self):
        form = self.cls_form()
        # print('-'*20)
        # print(form.as_p())
        # print('-'*20)
        self.assertIn('Материнська тека:', form.as_p())
        self.assertIn('Тека:', form.as_p())
        self.assertIn('Дата створення:', form.as_p())
        self.assertIn('option value="" selected="selected"', form.as_p())

    def test_form_renders_values(self):
        form = self.cls_form(data=self.initial_data)
        self.assertIn('option value="1" selected="selected">dummy_root_folder', form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data=self.empty_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_FIELD_ERROR])

    # TODO-не перевіряється умова unique_together = (("parent", "name"),)
    # FolderCreate не показує * на обов'язковому полі name (а FolderUpdate - показує).
    # Після Submit переадресовує ще раз на folders/create.
    # Нову теку з іменем-дублікатом не створює.
    # @skip
    def test_form_validation_for_duplicate_fields(self):
        DummyFolder().create_dummy_folder(name='dummy-1')
        data = {'name': "dummy-1"}
        form = self.cls_form(data=data)
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertEqual(form.errors['parent'], [DUPLICATE_ITEM_ERROR])
        self.assertEqual(form.errors['name'], [DUPLICATE_ITEM_ERROR])




# --------------------------------------------------------------
class ItemFormTest(TestCase):

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
