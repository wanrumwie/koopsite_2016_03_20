from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
from folders.models import Folder
from functional_tests_koopsite.base import FunctionalTest


class IndexVisitorTest(FunctionalTest):

    def test_layout_and_styling_index_page(self):
        # Edith goes to the home page
        self.browser.get('%s%s' % (self.server_url, '/index/'))
        self.browser.set_window_size(1024, 800)

        # She notices the input box is nicely centered
        box = self.browser.find_element_by_id('site-header')
        self.assertAlmostEqual(
            box.location['x'] + box.size['width'] / 2, 512, delta=10,
            msg="Не працює CSS."
            )

    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, '/index/'))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

    # TODO-Error 404 for /folders/1/contents
    # TODO-Перевірка на 404 - тут чи в unitest?
    url_from = '/index/'
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
        self.browser.get('%s%s' % (self.server_url, '/index/'))
        elements = self.browser.find_elements_by_tag_name('a')
        self.assertEqual(len(elements),
                         len(self.links_for_anonymous_user),
                         msg="Кількість лінків на сторінці не відповідає очікуваній")

    def test_anonymous_user_can_go_to_links(self):
        # Незалогінений користувач може перейти по лінках на сторінці
        for link_parent_selector, link_text, expected_regex \
                in self.links_for_anonymous_user:
            self.check_go_to_link(self.url_from,
                link_parent_selector, link_text, expected_regex)
    '''
    def test_authentificated_user_can_go_to_links(self):
        # Залогінений користувач може перейти по лінках на сторінці
        for link_parent_selector, link_text, expected_regex \
                in self.links_for_authentificated_user:
            self.check_go_to_link(url_from,
                link_parent_selector, link_text, expected_regex)
    '''



