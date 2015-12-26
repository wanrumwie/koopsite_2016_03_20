import inspect
from unittest.case import skipIf
from django.contrib.auth.models import AnonymousUser
from folders.models import Folder
from folders.tests.test_base import DummyFolder
from folders.views import FolderParentList
from functional_tests_koopsite.ft_base import PageVisitTest
from koopsite.functions import round_up_division
from koopsite.settings import SKIP_TEST



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderParentListPageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/parents/'
    page_title  = 'Пасічний'
    page_name   = 'Список кореневих тек'

    def links_in_template(self, user):
        # Повертає список словників, які поступають як параметри до функції self.check_go_to_link(...)
        #     def check_go_to_link(self, this_url, link_parent_selector, link_text,
        #                           expected_regex=None, url_name=None, kwargs=None):
        # Ключі словників скорочені до 2-х літер: ls lt er un kw
        # плюс cd - condition для перевірки видимості лінка (буде аргументом ф-ції eval() ).
        # Спочатку визначаються деякі параметри:
        username, flat_id, flat_No = self.get_user_name_flat(user)
        s = [
            {'ls':'#body-navigation'          , 'lt': 'Головна сторінка', 'un': 'index'},
            {'ls':'#body-navigation'          , 'lt': 'Картотека (ст.)' , 'un': 'folders:folder-list-all'},
            {'ls':'#body-navigation'          , 'lt': 'Теки'            , 'un': 'folders:folder-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Кореневі теки'   , 'un': 'folders:folder-parents'},
            {'ls':'#body-navigation'          , 'lt': 'Файли'           , 'un': 'folders:report-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Нова тека'       , 'un': 'folders:folder-create'},
            # {'ls':'#body-navigation'          , 'lt': 'Новий файл'      , 'un': 'folders:report-upload'},
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (js)'  , 'un': 'folders:folder-contents', 'kw': {'pk': 1}, 'st': 5},
            # {'ls':'#body-navigation'          , 'lt': 'Назад'           , 'un': "javascript:history.back()"},
            {'ls':'#header-aside-2-navigation', 'lt': username          , 'un': 'own-profile' , 'cd': "user.is_authenticated()"},
            {'ls':'#header-aside-2-navigation', 'lt': "Кв." + flat_No   , 'un': "flats:flat-detail", 'kw': {'pk': flat_id}, 'cd': "user.is_authenticated() and user.userprofile.flat"},
            {'ls':'#header-aside-2-navigation', 'lt': 'Вийти'           , 'un': 'logout'      , 'cd': "user.is_authenticated()", 'er': '/index/'},
            {'ls':'#header-aside-2-navigation', 'lt': 'Авторизуватися'  , 'un': 'login'       , 'cd': "not user.is_authenticated()"},
            ]
        return s

    def get_data_length(self):
        self.data_length = len(Folder.objects.filter(parent=None))# довжина списку з даними
        return self.data_length

    def get_num_page_links(self):
        # Повертає к-ть сторінок і к-ть лінків пейджінатора
        paginate_by = FolderParentList.paginate_by
        if paginate_by:
            num_pages = round_up_division(self.get_data_length(), paginate_by)
            if   num_pages == 1: page_links_number = 0
            elif num_pages == 2: page_links_number = 1
            else: page_links_number = 2
        else:
            num_pages = 1
            page_links_number = 0
        return num_pages, page_links_number

    def get_data_links_number(self):
        self.data_links_number = self.get_data_length() # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += self.get_num_page_links()[1]
        self.data_links_number += 1 # лінк javascript:history.back()
        return self.data_links_number


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderParentListPageAuthenticatedVisitorTest(FolderParentListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFolder().create_dummy_catalogue()
        self.get_data_links_number()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_can_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_visit_page()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    # @skip
    def test_layout_and_styling_page(self):
        # CSS завантажено і працює
        self.layout_and_styling_page()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    # @skip
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderParentListPageAnonymousVisitorTest(FolderParentListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFolder().create_dummy_catalogue()
        self.get_data_links_number()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderParentListPageAuthenticatedVisitorCanFindLinkTest(FolderParentListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        DummyFolder().create_dummy_catalogue()
        self.get_data_links_number()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_visitor_can_find_folder(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Folder.objects.filter(parent=None):
            link_parent_selector = '#body-list'
            link_text            = f.name
            url_name             = 'folders:folder-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = ""
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderParentListPageAnonymousVisitorCanFindLinkTest(FolderParentListPageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        DummyFolder().create_dummy_catalogue()
        self.get_data_links_number()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_visitor_can_find_folder(self):
        # Користувач може  перейти по лінку потрібні дані
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        for f in Folder.objects.filter(parent=None):
            link_parent_selector = '#body-list'
            link_text            = f.name
            url_name             = 'folders:folder-detail'
            kwargs               = {'pk': f.id}
            expected_regex       = "/noaccess/"
            self.check_go_to_link(self.this_url, link_parent_selector, link_text,
                url_name=url_name, kwargs=kwargs, expected_regex=expected_regex)
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

