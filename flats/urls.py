from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from koopsite.views import page_not_ready

from .views import FlatList, FlatScheme, \
                    FlatDetail, FlatDetailHorizontal, \
                    FlatTable
from .tables import PersonTableView

"""
/flats/ - під'єднано у модулі koopsite.urls.py:
            url(r'^flats/',   include('flats.urls')),
"""
urlpatterns = [
    # url(r'^person/table/$',   PersonTableView.as_view(), name='person-table'),
    url(r'^person/table/$',   page_not_ready, name='person-table'),
    url(r'^list/$',           FlatList.as_view(), name='flat-list'),
    url(r'^scheme/$',         FlatScheme.as_view(), name='flat-scheme'),
    url(r'^(?P<pk>[0-9]+)/$', FlatDetail.as_view(), name='flat-detail'),
    url(r'^(?P<pk>[0-9]+)/page(?P<page>\d+)/$',
                            FlatDetail.as_view(), name='flat-detail-page'),
    url(r'^(?P<pk>[0-9]+)/h/$',
                        FlatDetailHorizontal.as_view(), name='flat-detail-h'),
    url(r'^table/$',    FlatTable.as_view(),      name='flat-table'),
    url(r'^table/page(?P<page>\d+)/$',
                        FlatTable.as_view(),      name='flat-table-page'),
]
# urlpatterns += staticfiles_urlpatterns()

