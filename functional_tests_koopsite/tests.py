import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from koopsite.views import index


class IndexVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.implicitly_wait(30)
        pass
        # self.browser.refresh()
        # self.browser.quit()

    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

    # TODO-Error 404 for /folders/1/contents
    # TODO-Перевірка на 404 - тут чи в unitest?
    links_for_anonymous_user = [
        ('#body-navigation'          ,  'Квартири'          , '^flats/scheme/$'),
        ('#body-navigation'          ,  'Документи'         , '^folders/(?P<pk>[0-9]+)/contents/$'),
        ('#body-navigation'          ,  'Увійти'            , '^login/$'),
        ('#body-navigation'          ,  'Зареєструватися'   , '^register/$'),
        ('#header-aside-2-navigation',  'Авторизуватися'    , '^login/$'),
        ('#body-aside-1-navigation'  ,  'Увійти'            , '^login/$'),
        ('#body-aside-1-navigation'  ,  'Зареєструватися'   , '^register/$'),
    ]
    # TODO-зробити функц. тест для авторизованого користувача
    links_for_authentificated_user = [
        ('#body-navigation'          ,  'Квартири'          , '^flats/scheme/$'),
        ('#body-navigation'          ,  'Документи'         , '^folders/(?P<pk>[0-9]+)/contents/$'),
        ('#body-navigation'          ,  'Мій профіль'       , '^own/profile/$'),
        ('#body-navigation'          ,  'Адміністрування'   , '^adm/index/$'),
        ('#header-aside-2-navigation',  'Roman'             , '^own/profile/$'),
        ('#header-aside-2-navigation',  'Вийти'             , '^logout/$'),
    ]

    def test_anonymous_user_all_links_exist(self):
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        elements = self.browser.find_elements_by_tag_name('a')
        self.assertEqual(len(elements),
                         len(self.links_for_anonymous_user),
                         msg="Кількість лінків на сторінці не відповідає очікуваній")

    def check_go_to_link(self, link_parent_selector, link_text, expected_regex):
        # Користувач може перейти по лінку, заданому expected_regex
        # з текстом "link_text"
        self.browser.get('%s%s' % (self.live_server_url, '/index/'))
        # print(link_parent_selector, link_text, expected_regex)
        parent = self.browser.find_element_by_css_selector(
                                                link_parent_selector)
        href = parent.find_element_by_link_text(link_text)
        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
        passing_url = self.browser.current_url  # url після переходу
        expected_regex = expected_regex.lstrip('^')
        self.assertRegex(passing_url, expected_regex)

    def test_anonymous_user_can_go_to_links(self):
        # Незалогінений користувач може перейти по лінках на сторінці
        for link_parent_selector, link_text, expected_regex \
                in self.links_for_anonymous_user:
            self.check_go_to_link(
                link_parent_selector, link_text, expected_regex)




