from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from koopsite.templatetags.koop_template_filters import get_at_index, get_item_by_key, range_of
from koopsite.urls import urlpatterns

"""
Необхідність перевірки фільтрів виникає тому,
що Django не показує звичайних Python помилок у фільтрах,
бо вони працюють при рендерінгу шаблонів, коли, очевидно,
умови перевірки менш жорсткі, ніж Python.
Разом з тим, при тестуванні з доп. Selenium ці помилки виявляються.
Наприклад:
@register.filter()
def get_at_index(list, index):
    # Фільтр для отримання елемента списку за його індексом
    return list[index]


"""

class TemplateFiltersTest(TestCase):

    def test_get_at_index(self):
        list = [0,1,2,3]
        self.assertEqual(get_at_index(list, 0), 0)
        self.assertEqual(get_at_index('0123', 3), '3')
        self.assertIsNone(get_at_index(1234, 0))
        self.assertIsNone(get_at_index(list, 4))

    def test_get_item_by_key(self):
        d = {'1': 1, '2': 2}
        self.assertEqual(get_item_by_key(d, '1'), 1)
        self.assertIsNone(get_item_by_key(d, '3'))
        self.assertIsNone(get_item_by_key(d, 1))
        self.assertIsNone(get_item_by_key((1,2), 1))

    def test_range_of(self):
        self.assertEqual(range_of(1), range(1))
        self.assertEqual(range_of(-2), range(-2))
        self.assertIsNone(range_of((1,)))

