from django.conf.urls import url
from lists.views import view_list

from .views import home_page

"""
/lists/ - під'єднано у модулі koopsite.urls.py:
            url(r'^lists/',   include('lists.urls')),
"""
urlpatterns = [
    # url(r'^person/table/$',   PersonTableView.as_view(), name='person-table'),
    url(r'^$',   home_page, name='home'),
    url(r'^the-only-list-in-the-world/$', view_list, name='view_list'),
]
# urlpatterns += staticfiles_urlpatterns()

