from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, \
                       HASH_SESSION_KEY, get_user_model, authenticate
from django.contrib.auth.models import Permission
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys


class FunctionalTest(StaticLiveServerTestCase): # працює з окремою спеціально
                                                # створюваною БД для тестів
                                                # + статичні файли
    server_url = None       # резервуємо імена, які будуть
    this_url   = None       # означені в дочірніх класах

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)
        cls.browser.set_window_position(250, 0)
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        # cls.browser.refresh()
        # cls.browser.quit()
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass
        # self.browser.implicitly_wait(10)
        # self.browser.refresh()
        # self.browser.quit()

    def eval_condition(self, condition, user):
        # перевірка умови, заданої стрічкою
        # У складі стрічки можлива наявність виразів типу user.is_staff,
        # тому user приходить сюди як параметр
        if condition:
            try:    c = eval(condition)
            except: c = None
        else:
            c = True    # відсутність умови рівносильна виконанню умови
        return c

    def check_go_to_link(self, this_url, link_parent_selector, link_text,
                        url_name=None, kwargs=None, expected_regex=None):
        """
        Допоміжна функція для функц.тесту. Викликається в циклі for
        для кожного лінка на сторінці.
        Перевіряє, чи користувач може перейти по лінку, заданому url_name
        з текстом "link_text"
        :param this_url: сторінка що тестується
        :param link_parent_selector: CSS-селектор елемента з лінками
        :param link_text: видимий текст лінка
        :param url_name: назва, з якої ф-цією reverse отримується url переходу
        :param kwargs: евентуальні параметри url
        :param expected_regex: очікуваний url - задавати при переадресації, бо тоді він інакший, ніж reverse(url_name)
        :return:
        """
        self.browser.get('%s%s' % (self.server_url, this_url))
        # print(link_parent_selector, link_text, expected_regex)
        parent = self.browser.find_element_by_css_selector(
                                                link_parent_selector)
        href = parent.find_element_by_link_text(link_text)
        actions = ActionChains(self.browser)
        actions.move_to_element(href)
        actions.click(href)
        actions.perform()
        passing_url = self.browser.current_url  # url після переходу
        if url_name and not expected_regex:
            expected_regex = reverse(url_name, kwargs=kwargs)
        expected_regex = expected_regex.lstrip('^')
        # print('href =', href)
        # print('url_name =', url_name)
        # print('kwargs =', kwargs)
        # print('passing_url =', passing_url)
        # print('expected_regex =', expected_regex)
        self.assertRegex(passing_url, expected_regex)

def create_user_session(user):
    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session

def create_cookie(session):
    # Finally, create the cookie dictionary
    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': session.session_key,
        'secure': False,
        'path': '/',
    }
    return cookie

def add_cookie_to_browser(cookie, browser, server_url, url):
    # visit some url in your domain to setup Selenium.
    # (404 pages load the quickest)
    # self.browser.get('your-url' + '/404-non-existent/')
    browser.get('%s%s' % (server_url, url))

    # add the newly created session cookie to selenium webdriver.
    browser.add_cookie(cookie)

    # refresh to exchange cookies with the server.
    browser.refresh()

    # This time user should present as logged in.
    # self.browser.get('your-url')

def add_user_cookie_to_browser(user, browser, server_url, url="/"):
    session = create_user_session(user)
    cookie = create_cookie(session)
    add_cookie_to_browser(cookie, browser, server_url, url)


class DummyUser():
    def create_dummy_user(self,
                              username='dummy_user',
                              password='top_secret'
                            ):
        User = get_user_model()
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        permission = Permission.objects.get(name='Can activate/deactivate account')
        user.user_permissions.add(permission)

        # print('-'*50)
        # print('permission =', permission)
        print('created user:', user)
        #
        # user.is_staff = True
        user.save()
        self.dummy_user = user
        return user



class FunctionalTestAuthenticateUser(DummyUser, FunctionalTest):
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        add_user_cookie_to_browser(self.dummy_user, self.browser, self.server_url, "/")


