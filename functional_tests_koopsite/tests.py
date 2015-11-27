import time
from django.core.urlresolvers import reverse
from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# class NewVisitorTest(unittest.TestCase):
from selenium.webdriver.support.wait import WebDriverWait
from koopsite.views import index


class IndexVisitorTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(IndexVisitorTest, cls).setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(6)

    @classmethod
    def tearDownClass(cls):
        # time.sleep(5)
        cls.browser.quit()
        super(IndexVisitorTest, cls).tearDownClass()

    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

    def test_can_go_to_link_flats(self):
        # Користувач може перейти по лінку "Квартири"
        # Користувач може перейти по лінку "Документи"
        pass
