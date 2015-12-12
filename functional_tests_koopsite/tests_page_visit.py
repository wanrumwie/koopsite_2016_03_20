import inspect
from unittest.case import skip
from django.contrib.auth.models import AnonymousUser
from functional_tests_koopsite.ft_base import FunctionalTest, \
    DummyUser, DummyData, \
    add_user_cookie_to_browser


class IndexPageVisitTest(DummyUser, DummyData, FunctionalTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки головної сторінки сайту
    аутентифікованим користувачем.
    Цей клас буде використовуватися як основа
    для класів тестування інших сторінок.
    """
    this_url    = '/index/'
    page_title  = 'Пасічний'
    page_name   = 'Головна сторінка'
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url, "/")
        self.create_dummy_folder()

    def can_visit_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn(self.page_title, self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn(self.page_name, header_text)

    def expected_links_on_page(self, user):
        # Повертає список словників, які поступають як параметри до функції self.check_go_to_link(...)
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        # Спочатку визначаються деякі параметри:
        try:    username = user.username
        except: username = ""
        try:    flat_id = user.userprofile.flat.id
        except: flat_id = ""
        try:    flat_No = user.userprofile.flat.flat_No
        except: flat_No = ""
        s = [
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated()"},
            # {'ls':'#body-navigation'          , 'lt': 'Головна сторінка' , 'un': 'index'},##########
            {'ls':'#body-navigation'          , 'lt': 'Квартири'         , 'un': 'flats:flat-scheme'},
            {'ls':'#body-navigation'          , 'lt': 'Документи'        , 'un': 'folders:folder-contents', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Мій профіль'      , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#body-navigation'          , 'lt': 'Адміністрування'  , 'un': 'adm-index'   , 'cd': "user.has_perm('koopsite.activate_account')"},
            # {'ls':'#body-navigation'          , 'lt': 'Назад           ' , 'un': '"javascript:history.back()"'},#########
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        elements = self.browser.find_elements_by_tag_name('a')
        expected = 0
        for d in self.expected_links_on_page(self.dummy_user):
            condition            = d.get('cd')
            link_must_be_visible = self.eval_condition(condition, self.dummy_user)
            if link_must_be_visible :
                expected += 1
        self.assertEqual(len(elements), expected,
              msg="Кількість лінків на сторінці не відповідає очікуваній")

    def visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        # Беремо список словників, які описують всі лінки на цій сторінці.
        # Ключі словників скорочені до 2-х літер: ls lt er un kw cd.
        for d in self.expected_links_on_page(self.dummy_user):
            link_parent_selector = d.get('ls')
            link_text            = d.get('lt')
            url_name             = d.get('un')
            kwargs               = d.get('kw')
            expected_regex       = d.get('er')
            condition            = d.get('cd')
            link_must_be_visible = self.eval_condition(condition, self.dummy_user)
            if link_must_be_visible :
                self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                    url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)

    def layout_and_styling_page(self):
        # Користувач відвідує сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        self.browser.set_window_size(1024, 800)
        # Заголовок сайта добре відцентрований
        box = self.browser.find_element_by_id('site-header')
        real = box.location['x'] + box.size['width'] / 2
        expected = 512
        self.assertAlmostEqual(real, expected, delta=10, msg="Не працює CSS.")


class IndexPageAuthenticatedVisitorTest(IndexPageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем
    (такі параметри користувача і сторінки
    описані в суперкласі, тому не потребують переозначення)
    """
    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished:', inspect.stack()[0][3])

    def test_layout_and_styling_page(self):
        # CSS завантажено і працює
        self.layout_and_styling_page()
        print('finished:', inspect.stack()[0][3])

    def test_all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.all_links_on_page_exist()
        print('finished:', inspect.stack()[0][3])

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAuthenticatedVisitorWithFlatTest(IndexPageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з номером квартири)
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url, "/")
        self.create_dummy_folder()
        profile = self.create_dummy_profile(user=self.dummy_user)
        flat = self.create_dummy_flat()
        profile.flat=flat
        profile.save()

    def test_all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.all_links_on_page_exist()
        print('finished:', inspect.stack()[0][3])

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAuthenticatedVisitorWithPermissionTest(IndexPageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з доступом типу stuff
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url, "/")
        self.create_dummy_folder()
        self.add_dummy_permission(self.dummy_user,
                                  name='Can activate/deactivate account')

    def test_all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.all_links_on_page_exist()
        print('finished:', inspect.stack()[0][3])

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAnonymousVisitorTest(IndexPageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    анонімним користувачем
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        self.create_dummy_folder()

    def test_all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.all_links_on_page_exist()
        print('finished:', inspect.stack()[0][3])

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])
