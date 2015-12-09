from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, \
                       HASH_SESSION_KEY, get_user_model, authenticate
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys
# from functional_tests_koopsite.create_session_cookie import create_session_cookie


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

    def check_go_to_link(self,
            this_url, link_parent_selector, link_text,
            expected_regex=None,
            url_name=None, kwargs=None,
            condition=None):
        # Користувач може перейти по лінку, заданому expected_regex
        # з текстом "link_text"
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
        self.assertRegex(passing_url, expected_regex)
        # print('href =', href)
        print('passing_url =', passing_url)
        print('expected_regex =', expected_regex)
        print('url_name =', url_name)
        print('kwargs =', kwargs)
        print('condition =', condition)

'''
class FunctionalTestAuthenticateUser(FunctionalTest):
    def setUp(self):
        session_cookie = create_session_cookie(
            username='testuser', password='top_secret'
        )

        # visit some url in your domain to setup Selenium.
        # (404 pages load the quickest)
        # self.browser.get('your-url' + '/404-non-existent/')
        self.browser.get('%s%s' % (self.server_url, self.this_url))

        # add the newly created session cookie to selenium webdriver.
        print('self.browser =', self.browser)
        self.browser.add_cookie(session_cookie)
        print('self.browser =', self.browser)

        # refresh to exchange cookies with the server.
        self.browser.refresh()
        print('self.browser =', self.browser)

        # This time user should present as logged in.
        # self.browser.get('your-url')

'''

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
    # print('self.browser =', browser)
    browser.add_cookie(cookie)
    # print('self.browser =', browser)

    # refresh to exchange cookies with the server.
    browser.refresh()
    # print('self.browser =', browser)

    # This time user should present as logged in.
    # self.browser.get('your-url')

class DummyUser():
    def create_dummy_user(self,
                              username='dummy_user',
                              password='top_secret'
                            ):
        User = get_user_model()
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        user.is_staff = True
        self.dummy_user = user
        return user


class FunctionalTestAuthenticateUser(DummyUser, FunctionalTest):
    def setUp(self):
        self.dummy_user = self.create_dummy_user()
        session = create_user_session(self.dummy_user)
        cookie = create_cookie(session)
        add_cookie_to_browser(cookie, self.browser, self.server_url, "/")


