from unittest.case import skip
from selenium.webdriver.common.keys import Keys
from functional_tests_lists.base import ListsFunctionalTest


class LayoutAndStylingTestLists(ListsFunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get('%s%s' % (self.server_url, '/lists/'))
        self.browser.set_window_size(1024, 600)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        buttonbox = self.browser.find_element_by_id('submit_button')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2 ,
                                   # + buttonbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        buttonbox = self.browser.find_element_by_id('submit_button')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
                                   # + buttonbox.size['width'] / 2,
            512,
            delta=10
        )


