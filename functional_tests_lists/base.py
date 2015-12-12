from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
from functional_tests_koopsite.ft_base import FunctionalTest


class ListsFunctionalTest(FunctionalTest): # працює з окремою спеціально
                                                # створюваною БД для тестів
                                                # + статичні файли
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

