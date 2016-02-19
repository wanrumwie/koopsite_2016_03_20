from django.conf.urls import url
from django.views.generic.base import TemplateView

"""
/js_tests/ - під'єднано у модулі koopsite.urls.py:
    url(r'^js_tests/',  include('js_tests.urls')),
"""

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='js_tests.html'),
                                      name='js_tests'),
    url(r'^example/$',
        TemplateView.as_view(template_name='js_tests_example.html'),
                                      name='example'),
    url(r'^browtab/$',
        TemplateView.as_view(template_name='js_tests_browtab.html'),
                                      name='browtab'),

    url(r'^koopsite/functions/$',
        TemplateView.as_view(template_name='koopsite/js_tests_koopsite_functions.html'),
                                      name='koopsite_functions'),
    url(r'^koopsite/browtab/$',
        TemplateView.as_view(template_name='koopsite/js_tests_koopsite_browtab.html'),
                                      name='koopsite_browtab'),
    url(r'^folders/$',
        TemplateView.as_view(template_name='folders/js_tests_folders.html'),
                                      name='folders'),
]

