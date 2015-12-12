import inspect
from unittest.case import skip
from django.contrib.auth.models import AnonymousUser
from functional_tests_koopsite.ft_base import add_user_cookie_to_browser
from functional_tests_koopsite.tests_page_visit import IndexPageVisitTest


class FlatSchemePageVisitTest(IndexPageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту
    аутентифікованим користувачем.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/flats/scheme/'
    page_title  = 'Пасічний'
    page_name   = 'Схема розташування квартир'

    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url, "/flats/scheme/")

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
            {'ls':'#body-navigation'          , 'lt': 'Головна сторінка' , 'un': 'index'},
            # {'ls':'#body-navigation'          , 'lt': 'Схема розташування квартир', 'un': 'flats:flat-scheme'},#########
            {'ls':'#body-navigation'          , 'lt': 'Список квартир'   , 'un': 'flats:flat-list'},
            {'ls':'#body-navigation'          , 'lt': 'Таблиця параметрів всіх квартир'   , 'un': 'flats:flat-table'},
            {'ls':'#body-navigation'          , 'lt': 'Таблиця персон (в роботі!)'   , 'un': 'flats:person-table'},
            # {'ls':'#body-navigation'          , 'lt': 'Назад           ' , 'un': '"javascript:history.back()"'},
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No    , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

class FlatSchemePageAuthenticatedVisitorTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
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

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class FlatSchemePageAuthenticatedVisitorWithFlatTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
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

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class FlatSchemePageAnonymousVisitorTest(FlatSchemePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        self.create_dummy_folder()

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])
