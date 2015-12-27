from django.conf.urls import url
from django.views.generic.base import TemplateView

"""
/js_tests/ - під'єднано у модулі koopsite.urls.py:
    url(r'^js_tests/',  include('js_tests.urls')),
"""

urlpatterns = [
    url(r'^$',                  TemplateView.as_view(template_name='js_tests.html')),
    url(r'^koopsite/functions/$', TemplateView.as_view(template_name='js_tests_koopsite_functions.html')),
    url(r'^koopsite/browtab/$', TemplateView.as_view(template_name='js_tests_koopsite_browtab.html')),
    url(r'^lists/$',            TemplateView.as_view(template_name='js_tests_lists.html')),
    url(r'^folders/$',          TemplateView.as_view(template_name='js_tests_folders.html')),
]

