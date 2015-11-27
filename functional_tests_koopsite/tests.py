# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import reverse
from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import unittest

# class NewVisitorTest(unittest.TestCase):
from selenium.webdriver.support.wait import WebDriverWait
from koopsite.views import index


class IndexVisitorTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(IndexVisitorTest, cls).setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        # time.sleep(5)
        cls.browser.implicitly_wait(30)
        # cls.browser.quit()
        # super(IndexVisitorTest, cls).tearDownClass()

    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

    def check_go_to_link(self, link_text, expected_regex):
        # Користувач може перейти по лінку, заданому expected_regex
        # з текстом "link_text"
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        href = self.browser.find_element_by_link_text(link_text)
        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
        passing_url = self.browser.current_url  # url після переходу
        expected_regex = expected_regex.lstrip('^')
        self.assertRegex(passing_url, expected_regex)

    def test_unauthorized_user_can_go_to_links(self):
        # Незалогінений користувач може перейти по лінках на сторінці
        links = [
            ('Квартири'          , '^flats/scheme/$'),
            # ('Документи'         , '^folders/(?P<pk>[0-9]+)/contents/$'),
            ('Увійти'            , '^login/$'),
            ('Зареєструватися'   , '^register/$'),
            ('Авторизуватися'    , '^login/$'),
            # ('Увійти'            , '^login/$'),
            # ('Зареєструватися'   , '^register/$'),
            # ('Квартири'          , '^flats/scheme/$'),
            # ('Документи'         , '^folders/(?P<pk>[0-9]+)/contents/$'),
            # ('Мій профіль'       , '^own/profile/$'),
            # ('Адміністрування'   , '^adm/index/$'),
            # ('Roman'             , '^own/profile/$'),
            # ('Вийти'             , '^logout/$'),
        ]
        for link_text, expected_regex in links:
            self.check_go_to_link(link_text, expected_regex)


