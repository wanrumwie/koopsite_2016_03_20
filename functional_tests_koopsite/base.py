from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys


class FunctionalTest(StaticLiveServerTestCase): # працює з окремою спеціально
                                                # створюваною БД для тестів
                                                # + статичні файли
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

    def check_go_to_link(self, this_url, link_parent_selector, link_text, expected_regex):
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
        expected_regex = expected_regex.lstrip('^')
        self.assertRegex(passing_url, expected_regex)
        # print('href =', href)
        # print('passing_url =', passing_url)
        # print('expected_regex =', expected_regex)


