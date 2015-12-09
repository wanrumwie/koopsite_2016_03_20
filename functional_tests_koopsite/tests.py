import inspect
from unittest.case import skip
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from folders.models import Folder
from functional_tests_koopsite.base import FunctionalTest, FunctionalTestAuthenticateUser


class IndexVisitorTest(FunctionalTest):
    this_url = '/index/'
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

    @skip
    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

    @skip
    def test_layout_and_styling_index_page(self):
        # Користувач відвідує головну сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        self.browser.set_window_size(1024, 800)
        # Заголовок сайта добре відцентрований
        box = self.browser.find_element_by_id('site-header')
        real = box.location['x'] + box.size['width'] / 2
        expected = 512
        self.assertAlmostEqual(real, expected, delta=10, msg="Не працює CSS.")

    @skip
    def test_anonymous_user_all_links_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        elements = self.browser.find_elements_by_tag_name('a')
        self.assertEqual(len(elements),
                         len(self.links_for_anonymous_user),
                         msg="Кількість лінків на сторінці не відповідає очікуваній")

    @skip
    def test_anonymous_user_can_go_to_links(self):
        # Незалогінений користувач може перейти по всіх лінках на сторінці
        folder = Folder()
        folder.save()       # створюємо теку з id=1 для folders/1/contents/
        for link_parent_selector, link_text, expected_regex \
                in self.links_for_anonymous_user:
            self.check_go_to_link(self.this_url,
                link_parent_selector, link_text, expected_regex)


# TODO-зробити функц. тест для користувача: анонімного, авторизованого, stuff і т.д.
class IndexAuthenticatedVisitorTest(FunctionalTestAuthenticateUser):
    this_url = '/index/'
    links_on_page = [
        ('#body-navigation'          ,  'Квартири'          , 'flats:flat-scheme'),
        # ('#body-navigation'          ,  'Квартири'          , '^flats/scheme/$'),
        ('#body-navigation'          ,  'Документи'         , 'folders:folder-contents', None, {'pk': 1}),
        # ('#body-navigation'          ,  'Мій профіль'       , '^own/profile/$'),
        ('#body-navigation'          ,  'Мій профіль'       , 'own-profile'),
        ('#body-navigation'          ,  'Адміністрування'   , 'adm-index'),
        ('#header-aside-2-navigation',  'Roman'             , 'own-profile'),
        ('#header-aside-2-navigation',  'Вийти'             , 'logout'),

        # ('#body-navigation'          ,  'Увійти'            , '^login/$'),
        # ('#body-navigation'          ,  'Зареєструватися'   , '^register/$'),
        # ('#header-aside-2-navigation',  'Авторизуватися'    , '^login/$'),
        # ('#body-aside-1-navigation'  ,  'Увійти'            , '^login/$'),
        # ('#body-aside-1-navigation'  ,  'Зареєструватися'   , '^register/$'),
    ]

    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)

        is_auth = self.dummy_user.is_authenticated
        is_staff = self.dummy_user.is_staff
        try:    flat = self.dummy_user.userprofile.flat
        except: flat = "---"
        print('is_auth =', is_auth)
        print('is_auth =', is_auth.__self__)
        print('is_auth =', is_auth.__func__)
        print('is_staff =', is_staff)
        print('flat =', flat)
        s = 'is_staff'
        u = 'self.dummy_user'
        e = '%s.%s' % (u, s)
        r = eval(e)
        print('s=', s)
        print('u=', u)
        print('e=', e)
        print('r=', r)

        print('finished:', inspect.stack()[0][3])

    @skip
    def test_layout_and_styling_index_page(self):
        # Користувач відвідує головну сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        self.browser.set_window_size(1024, 800)
        # Заголовок сайта добре відцентрований
        box = self.browser.find_element_by_id('site-header')
        real = box.location['x'] + box.size['width'] / 2
        expected = 512
        self.assertAlmostEqual(real, expected, delta=10, msg="Не працює CSS.")
        print('finished:', inspect.stack()[0][3])


    def test_authenticated_user_can_go_to_links(self):
        # Залогінений користувач може перейти по всіх лінках на сторінці
        folder = Folder()
        folder.save()       # створюємо теку з id=1 для folders/1/contents/

        for t in self.links_on_page:
            link_parent_selector = t[0]
            link_text            = t[1]
            url_name             = t[2]
            try:    condition = t[3]
            except: condition = None
            try:    kwargs = t[4]
            except: kwargs = None
            self.check_go_to_link(self.this_url,
                link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs,
                condition=condition)

        print('finished:', inspect.stack()[0][3])
            # {% if request.user.is_authenticated %}
            # {% if request.user.userprofile.flat %}


