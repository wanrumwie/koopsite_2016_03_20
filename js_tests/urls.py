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
    url(r'^browtab/$',
        TemplateView.as_view(template_name='js_tests_browtab.html'),
                                      name='browtab'),
    url(r'^browtab_ajax/$',
        TemplateView.as_view(template_name='js_tests_browtab_ajax.html'),
                                      name='browtab_ajax'),

    url(r'^functions/$',
        TemplateView.as_view(template_name='js_tests_functions.html'),
                                      name='functions'),
    url(r'^koopsite/users_browtab/$',
        TemplateView.as_view(template_name='koopsite/js_tests_users_browtab.html'),
                                      name='koopsite_users_browtab'),
    url(r'^folders/$',
        TemplateView.as_view(template_name='folders/js_tests_folders.html'),
                                      name='folders'),
    url(r'^example/$',
        TemplateView.as_view(template_name='js_tests_example.html'),
                                      name='example'),
]

