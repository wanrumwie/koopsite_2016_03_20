'''
Означення власних "фільтрів", якими можна користатися в шаблонах
'''
from django.template import Library

register = Library()

@register.filter()
def get_at_index(list, index):
    # Фільтр для отримання елемента списку за його індексом
    return list[index]

@register.filter()
def get_item_by_key(dictionary, key):
    # Фільтр для отримання значення словника за його ключем
    return dictionary.get(key)