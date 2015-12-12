import inspect
from unittest.case import skip
from folders.models import Folder
from functional_tests_koopsite.base import FunctionalTest, FunctionalTestAuthenticateUser


# TODO-зробити функц. тест для користувача: анонімного, авторизованого, stuff і т.д.
class IndexVisitorTest(FunctionalTestAuthenticateUser):
    this_url      = '/index/'
    # dummy_user    = None
    def expected_links_on_page(self, user):
        # Повертає список словників, які поступають як параметри до функції self.check_go_to_link(...)
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        # Спочатку визначаються деякі параметри:
        try:    username = user.username
        except: username = ""
        try:    userflat = user.userprofile.flat.flat_No
        except: userflat = ""
        s = [
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated"},
            {'ls':'#body-aside-1-navigation'  , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated"},
            # {'ls':'#body-navigation'          , 'lt': 'Головна сторінка' , 'un': 'index'},##########
            {'ls':'#body-navigation'          , 'lt': 'Квартири'         , 'un': 'flats:flat-scheme'},
            {'ls':'#body-navigation'          , 'lt': 'Документи'        , 'un': 'folders:folder-contents', 'kw': {'pk': 1}},
            {'ls':'#body-navigation'          , 'lt': 'Увійти'           , 'un': 'login'       , 'cd': "not user.is_authenticated"},
            {'ls':'#body-navigation'          , 'lt': 'Зареєструватися'  , 'un': 'register'    , 'cd': "not user.is_authenticated"},
            {'ls':'#body-navigation'          , 'lt': 'Мій профіль'      , 'un': 'own-profile' , 'cd': "user.is_authenticated"},
            {'ls':'#body-navigation'          , 'lt': 'Адміністрування'  , 'un': 'adm-index'   , 'cd': "user.has_perm('koopsite.activate_account')"},
            # {'ls':'#body-navigation'          , 'lt': 'Назад           ' , 'un': '"javascript:history.back()"'},#########
            {'ls':'#header-aside-2-navigation', 'lt': username           , 'un': 'own-profile' , 'cd': "user.is_authenticated"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + userflat   , 'un': "flats:flat-detail", 'kw': 'user.userprofile.flat.id', 'cd': "user.is_authenticated and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'            , 'un': 'logout'      , 'cd': "user.is_authenticated", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'   , 'un': 'login'       , 'cd': "not user.is_authenticated"},
            ]
        return s
    '''
    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)
        print('finished:', inspect.stack()[0][3])

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

    def test_all_links_on_page_exist(self):
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
    '''

    def test_visitor_can_go_to_links(self):
        # Залогінений користувач може перейти по всіх лінках на сторінці
        folder = Folder()
        folder.save()       # створюємо теку з id=1 для folders/1/contents/
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
        print('finished:', inspect.stack()[0][3])

'''
class IndexAuthenticatedVisitorTest(FunctionalTestAuthenticateUser):
'''

