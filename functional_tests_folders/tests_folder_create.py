import inspect
from unittest.case import skipIf
from django.contrib.auth.models import AnonymousUser
from folders.models import Folder
from folders.tests.test_base import DummyFolder
from functional_tests_koopsite.ft_base import PageVisitTest
from koopsite.settings import SKIP_TEST
from selenium.webdriver.common.keys import Keys


# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageVisitTest(PageVisitTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки одної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування цієї сторінки з іншими користувачами.
    """
    this_url    = '/folders/create/'
    page_title  = 'Пасічний'
    page_name   = 'Створення теки'

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
            # {'ls':'#body-navigation'          , 'lt': 'Картотека (ст.)' , 'un': 'folders:folder-list-all'},
            # {'ls':'#body-navigation'          , 'lt': 'Теки'            , 'un': 'folders:folder-list'},
            # {'ls':'#body-navigation'          , 'lt': 'Кореневі теки'   , 'un': 'folders:folder-parents'},
            # {'ls':'#body-navigation'          , 'lt': 'Файли'           , 'un': 'folders:report-list'},
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

    def get_data_links_number(self):
        self.data_links_number = 0 # кількість лінків, які приходять в шаблон з даними
        self.data_links_number += 2 # Кнопки
        self.data_links_number += 1 # лінк javascript:history.back()
        return self.data_links_number


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        # DummyFolder().create_dummy_catalogue()
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
class FolderCreatePageAnonymousVisitorTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    анонімним користувачем
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


@skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorWoPermissionTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    аутентифікованим користувачем без належного доступу
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_can_not_visit_page(self):
        # Заголовок і назва сторінки правильні
        self.can_not_visit_page()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))



# @skipIf(SKIP_TEST, "пропущено для економії часу")
class FolderCreatePageAuthenticatedVisitorCanCreateFolderTest(FolderCreatePageVisitTest):
    """
    Тест відвідання сторінки сайту
    користувачем
    Чи всі дані правильно відображені?
    Параметри сторінки описані в суперкласі, тому не потребують переозначення.
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        self.add_user_cookie_to_browser(self.dummy_user)
        self.add_dummy_permission(self.dummy_user, codename='add_folder', model='folder')
        DummyFolder().create_dummy_catalogue()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def test_visitor_can_create_folder(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Бачить у полі очікувану інформацію
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.is_selected():
                self.assertEqual(option.get_attribute('value'), '')

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає ENTER
        inputbox.send_keys(Keys.ENTER)

        passing_url = self.browser.current_url  # url після переходу
        expected_regex = "/folders/list/"
        self.assertRegex(passing_url, expected_regex)

        folder = Folder.objects.last()
        print('folder =', folder)
        self.assertEqual(folder.name, 'New_folder')
        self.assertIsNone(folder.parent)
        # Час створення (до секунди) співпадає з поточним?
        # print('folder.created_on =', folder.created_on, now())
        # self.assertAlmostEqual(folder.created_on, now(), delta=timedelta(minutes=1))

        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


    def test_visitor_can_create_folder_in_parent(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()
                parent_name = option.text

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає ENTER
        inputbox.send_keys(Keys.ENTER)

        passing_url = self.browser.current_url  # url після переходу
        expected_regex = "/folders/list/"
        self.assertRegex(passing_url, expected_regex)

        folder = Folder.objects.last()
        print('folder =', folder)
        self.assertEqual(folder.name, 'New_folder')
        self.assertEqual(folder.parent.id, 1)

        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


    def test_visitor_can_create_folder_in_parent_submit_button(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # Вибирає значення
        inputbox = self.browser.find_element_by_id('id_parent')

        all_options = inputbox.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute('value') == "1" :
                option.click()
                parent_name = option.text

        # Вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('New_folder')

        # Натискає кнопку submit
        button = self.browser.find_element_by_css_selector('input[type=submit]')
        button.click()

        passing_url = self.browser.current_url  # url після переходу
        expected_regex = "/folders/list/"
        self.assertRegex(passing_url, expected_regex)

        folder = Folder.objects.last()
        print('folder =', folder)
        self.assertEqual(folder.name, 'New_folder')
        self.assertEqual(folder.parent.id, 1)

        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


    def test_error_message_if_empty(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # НЕ вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')

        # Натискає ENTER
        inputbox.send_keys(Keys.ENTER)

        error = self.get_error_element(".errorlist")
        self.assertEqual(error.text, "Це поле обов'язкове.")

        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))


    def test_error_messages_are_cleared_on_input(self):
        # Користувач відкриває сторінку
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # НЕ вводить у полі дані
        inputbox = self.browser.find_element_by_id('id_name')

        # Натискає ENTER
        inputbox.send_keys(Keys.ENTER)

        # Виникає помилка
        error = self.get_error_element('.errorlist')
        self.assertTrue(error.is_displayed())

        # Починає вводити щоб виправити помилку
        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('a')

        # Повідомлення про помилку зникає
        error = self.get_error_element('.errorlist')
        self.assertFalse(error.is_displayed())

        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

