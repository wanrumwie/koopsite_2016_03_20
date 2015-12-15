import inspect
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
import time
from flats.models import Flat
from folders.models import Folder
from koopsite.functions import trace_print, print_list
from koopsite.models import UserProfile


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)


class FunctionalTest(StaticLiveServerTestCase): # працює з окремою спеціально
                                                # створюваною БД для тестів
                                                # + статичні файли
    server_url = None       # резервуємо імена, які будуть
    this_url   = None       # означені в дочірніх класах

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(20)
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
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
        cls.browser.quit()

    # def setUp(self):
    #     pass

    def tearDown(self):
        super().tearDown()
        print('finished: %-30s of %s' % (inspect.stack()[0][3], self.__class__.__name__))

    def add_user_cookie_to_browser(self, user, url=None):
        session = create_user_session(user)
        cookie = create_cookie(session)
        # visit some url in your domain to setup Selenium.
        if not url: url = '/selenium-cookie-setup/'
        self.browser.get('%s%s' % (self.server_url, url))
        # add the newly created session cookie to selenium webdriver.
        self.browser.add_cookie(cookie)
        # refresh to exchange cookies with the server.
        self.browser.refresh()

    def eval_condition(self, condition, user):
        # перевірка умови, заданої стрічкою
        # У складі стрічки можлива наявність виразів типу user.is_staff,
        # тому user приходить сюди як параметр
        if condition:
            try:    c = eval(condition)
            except: c = None
        else:
            c = True    # відсутність умови рівносильна виконанню умови
        # print('user =', user, 'cd =', condition, 'eval =', c)
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
        #
        # TODO-виловити помилку при очікуванні на сторінку "Документи" головної сторінки.
        # Помилка виникає часом. 
        # Trace:
        # selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: xhrErrorAlert:
        #  xhr.status=0
        #  xhr.statusText=error
        #  xhr.responseText={"server_response": {"selRowIndex": 0, "model": null, "id": null}}
        #
        parent = self.browser.find_element_by_css_selector(link_parent_selector)
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

    def get_link_location(self, link_parent_selector, link_text):
        parent = self.browser.find_element_by_css_selector(
                                                link_parent_selector)
        href = parent.find_element_by_link_text(link_text)
        location = href.location
        size = href.size
        return location, size


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


class DummyUser():
    def create_dummy_user(self,
                              username='dummy_user',
                              password='top_secret'
                            ):
        User = get_user_model()
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        user.save()
        self.dummy_user = user
        trace_print('created user:', user)
        return user

    def add_dummy_permission(self, user, name='Can activate/deactivate account'):
        permission = Permission.objects.get(name=name)
        user.user_permissions.add(permission)
        user.save()
        # print('-'*50)
        # print('permission =', permission)
        #
        # user.is_staff = True
        trace_print('added permission:', permission, 'for user:', user)
        return permission

    def create_dummy_profile(self, user):
        profile = UserProfile(user=user)
        profile.save()
        trace_print('created profile:', profile, 'for user:', user)
        return profile


class DummyData():
    # Створення в базі додаткових даних, потрібних для конкретного класу тестів
    def create_dummy_flat(self, flat_No="25а", floor_No=2,
                                entrance_No=3, flat_99=25):
        # створюємо квартиру:
        flat = Flat(flat_No=flat_No, floor_No=floor_No,
                    entrance_No=entrance_No, flat_99=flat_99)
        flat.save()
        # print('created flat:', flat)
        return flat

    def create_dummy_building(self, floors=(0,1,2,), entrances=(1,2,3,)):
        for f in floors:
            for e in entrances:
                for i in range(f+e):
                    no = f*100 + e*10 + i+1
                    flat_No = str(no)
                    # створюємо квартиру:
                    flat = Flat(flat_No=flat_No, floor_No=f,
                                entrance_No=e, flat_99=no)
                    flat.save()
        # print('created building')

    def create_dummy_folder(self):
        # Створення в базі додаткових даних, потрібних для конкретного класу тестів
        # створюємо теку з id=1 для folders/1/contents/:
        folder = Folder(name="dummy_root_folder", id=1)
        folder.save()
        # print('created folder:', folder)
        return folder


class PageVisitTest(DummyUser, DummyData, FunctionalTest):
    """
    Допоміжний клас для функціональних тестів.
    Описані тут параметри - для перевірки головної сторінки сайту.
    Цей клас буде використовуватися як основа
    для класів тестування інших сторінок.
    """
    this_url    = '/index/'
    page_title  = 'Пасічний'
    page_name   = 'Головна сторінка'
    data_links_number = 0   # кількість лінків, які приходять в шаблон з даними

    def can_visit_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn(self.page_title, self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn(self.page_name, header_text)

    def links_in_template(self, user):
        # Перелік лінків, важливих для сторінки.
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

    def visitor_can_go_to_links(self):
        # Лінки, вказані в шаблоні (в т.ч. і недоступні через умову if):
        links =  self.links_in_template(self.dummy_user)
        # Сторінка має всі передбачені лінки (по кількості)
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        elements = self.browser.find_elements_by_tag_name('a')
        visible_links = []
        for d in links:
            condition = d.get('cd')
            link_must_be_visible = self.eval_condition(condition, self.dummy_user)
            if link_must_be_visible :
                visible_links.append(d)
        expected = len(visible_links)
        expected += self.data_links_number # + лінки в таблицях з даними. Ці лінки даних не входять до словника links_in_template.
        # print_list('links', links)
        # print_list('visible_links', visible_links)
        # print_list('expected =', expected)
        self.assertEqual(len(elements), expected,
              msg="Кількість лінків на сторінці не відповідає очікуваній")
        # Користувач може перейти по всіх лінках на сторінці
        # Беремо список словників, які описують всі лінки на цій сторінці.
        # Ключі словників скорочені до 2-х літер: ls lt er un kw cd.
        for d in visible_links:
            link_parent_selector = d.get('ls')
            link_text            = d.get('lt')
            url_name             = d.get('un')
            kwargs               = d.get('kw')
            expected_regex       = d.get('er')
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


