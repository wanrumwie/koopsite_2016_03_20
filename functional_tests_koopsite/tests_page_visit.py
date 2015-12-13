import inspect
from unittest.case import skip
from django.contrib.auth.models import AnonymousUser
from functional_tests_koopsite.ft_base import add_user_cookie_to_browser, \
                                                PageVisitTest
from koopsite.functions import print_list


class IndexPageAuthenticatedVisitorTest(PageVisitTest):
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

    # def test_all_links_on_page_exist(self):
    #     # Сторінка має всі передбачені лінки (по кількості)
    #     self.all_links_on_page_exist()
    #     print('finished:', inspect.stack()[0][3])
    #
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAuthenticatedVisitorWithFlatTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з номером квартири)
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url)
        self.create_dummy_folder()
        profile = self.create_dummy_profile(user=self.dummy_user)
        flat = self.create_dummy_flat()
        profile.flat=flat
        profile.save()

    # def test_all_links_on_page_exist(self):
    #     # Сторінка має всі передбачені лінки (по кількості)
    #     self.all_links_on_page_exist()
    #     print('finished:', inspect.stack()[0][3])
    #
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAuthenticatedVisitorWithPermissionTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    аутентифікованим користувачем з доступом типу stuff
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url)
        self.create_dummy_folder()
        self.add_dummy_permission(self.dummy_user,
                                  name='Can activate/deactivate account')

    # def test_all_links_on_page_exist(self):
    #     # Сторінка має всі передбачені лінки (по кількості)
    #     self.all_links_on_page_exist()
    #     print('finished:', inspect.stack()[0][3])
    #
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])


class IndexPageAnonymousVisitorTest(PageVisitTest):
    """
    Тест відвідання головної сторінки сайту
    анонімним користувачем
    (параметри сторінки описані в суперкласі, тому не потребують переозначення)
    Переозначуємо параметри користувача:
    """
    def setUp(self):
        self.dummy_user = AnonymousUser()
        self.create_dummy_folder()

    # def test_all_links_on_page_exist(self):
    #     # Сторінка має всі передбачені лінки (по кількості)
    #     self.all_links_on_page_exist()
    #     print('finished:', inspect.stack()[0][3])
    #
    def test_visitor_can_go_to_links(self):
        # Користувач може перейти по всіх лінках на сторінці
        self.visitor_can_go_to_links()
        print('finished:', inspect.stack()[0][3])

# TODO-додати перевірку секції справа: Оголошення, Новини, ...
