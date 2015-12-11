import inspect
from unittest.case import skip
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, _user_has_perm
from django.http.request import HttpRequest
from folders.models import Folder
from functional_tests_koopsite.base import FunctionalTest, FunctionalTestAuthenticateUser

def eval_condition(condition, user):
    # перевірка умови, заданої стрічкою
    # У складі стрічки можлива наявність виразів типу user.is_staff,
    # тому user приходить сюди як параметр
    if condition:
        try:    c = eval(condition)
        except: c = None
    else:
        c = True    # відсутність умови рівносильна виконанню умови
    return c


# TODO-зробити функц. тест для користувача: анонімного, авторизованого, stuff і т.д.
class IndexVisitorTest(FunctionalTestAuthenticateUser):
    this_url      = '/index/'
    # dummy_user    = None
    def expected_links_on_page(self, user):
        try: username = user.username
        except: username = ""
        try: userflat = user.userprofile.flat.flat_No
        except: userflat = ""
        s = [
        ('#body-aside-1-navigation'  ,  'Увійти'            , 'login'       , '', "not user.is_authenticated"),
        ('#body-aside-1-navigation'  ,  'Зареєструватися'   , 'register'    , '', "not user.is_authenticated"),
        ## ('#body-navigation'          ,  'Головна сторінка'  , 'index'),
        ('#body-navigation'          ,  'Квартири'          , 'flats:flat-scheme'),
        ('#body-navigation'          ,  'Документи'         , 'folders:folder-contents', {'pk': 1}),
        # ('#body-navigation'          ,  'Увійти'            , 'login'       , '', "not user.is_authenticated"),
        # ('#body-navigation'          ,  'Зареєструватися'   , 'register'    , '', "not user.is_authenticated"),
        # ('#body-navigation'          ,  'Мій профіль'       , 'own-profile' , '', "user.is_authenticated"),
        ('#body-navigation'          ,  'Адміністрування'   , 'adm-index'   , '', "user.is_staff or user.has_perm('koopsite.activate_account')"),
        ## ('#body-navigation'          ,  'Назад           '  , '"javascript:history.back()"'),
        # ('#header-aside-2-navigation',  username            , 'own-profile' , '', "user.is_authenticated"),
        # ('#header-aside-2-navigation',  "Кв." + userflat    , "flats:flat-detail", 'user.userprofile.flat.id', "user.is_authenticated and user.userprofile.flat"),
        # ('#header-aside-2-navigation',  'Вийти'             , 'logout'      , '', "user.is_authenticated"),
        # ('#header-aside-2-navigation',  'Авторизуватися'    , 'login'       , '', "not user.is_authenticated"),
        ]
        return s

    @skip
    def test_can_visit_site_index_page(self):
        # Користувач може відвідати головну сторінку сайта
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        # Ця сторінка справді є сторінкою потрібного сайту
        self.assertIn('Пасічний', self.browser.title)
        # Цe головна сторінка
        header_text = self.browser.find_element_by_id('page-name').text
        self.assertIn('Головна сторінка', header_text)
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

    @skip
    def test_all_links_on_page_exist(self):
        # Сторінка має всі передбачені лінки (по кількості)
        self.browser.get('%s%s' % (self.server_url, self.this_url))
        elements = self.browser.find_elements_by_tag_name('a')
        expected = 0
        for t in self.expected_links_on_page(self.dummy_user):
            try:       condition = t[4]
            except:    condition = None
            link_must_be_visible = eval_condition(condition, self.dummy_user)
            print('link_must_be_visible =', link_must_be_visible)
            if link_must_be_visible :
                expected += 1
        self.assertEqual(len(elements), expected,
              msg="Кількість лінків на сторінці не відповідає очікуваній")


    def test_visitor_can_go_to_links(self):
        # Залогінений користувач може перейти по всіх лінках на сторінці
        folder = Folder()
        folder.save()       # створюємо теку з id=1 для folders/1/contents/

        # is_auth = self.dummy_user.is_authenticated
        # is_staff = self.dummy_user.is_staff
        # try:    flat = self.dummy_user.userprofile.flat
        # except: flat = "---"
        # try:    perm = self.dummy_user.has_perm('koopsite.activate_account')
        # except: perm = None
        #
        # print('is_auth =', is_auth)
        # print('is_auth =', is_auth.__self__)
        # print('is_auth =', is_auth.__func__)
        # print('is_staff =', is_staff)
        # print('flat =', flat)
        # print('perm =', perm)
        # s = 'is_staff'
        # u = 'self.dummy_user'
        # e = '%s.%s' % (u, s)
        # r = eval(e)
        # print('s=', s)
        # print('u=', u)
        # print('e=', e)
        # print('r=', r)

        for t in self.expected_links_on_page(self.dummy_user):
            print('t =', t)
            link_parent_selector = t[0]
            link_text            = t[1]
            url_name             = t[2]
            try:       kwargs    = t[3]
            except:    kwargs    = None
            try:       condition = t[4]
            except:    condition = None
            link_must_be_visible = eval_condition(condition, self.dummy_user)
            print('link_must_be_visible =', link_must_be_visible)
            if link_must_be_visible :
                self.check_go_to_link(self.this_url,
                    link_parent_selector, link_text,
                    url_name=url_name, kwargs=kwargs,
                    condition=condition)

        print('finished:', inspect.stack()[0][3])

'''
class IndexAuthenticatedVisitorTest(FunctionalTestAuthenticateUser):
'''

