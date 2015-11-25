from django.conf.urls import url

from .views import home_page

"""
/lists/ - під'єднано у модулі koopsite.urls.py:
            url(r'^lists/',   include('lists.urls')),
"""
urlpatterns = [
    # url(r'^person/table/$',   PersonTableView.as_view(), name='person-table'),
    url(r'^$',   home_page, name='home'),
]
# urlpatterns += staticfiles_urlpatterns()

