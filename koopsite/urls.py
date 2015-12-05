"""koopsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from koopsite.views import UserPermsActivateUpdate, OwnProfileDetailShow, UserProfileDetailShow
from koopsite.viewsajaxuser import UsersTable, AjaxRecognizeAccount, \
                    AjaxDenyAccount, AjaxActivateAccount, \
                    AjaxDeactivateAccount, AjaxDeleteAccount, \
                    AjaxSetMemberAccount, AjaxDenyMemberAccount, \
                    AjaxActivateAllAccounts, AjaxSetMemberAllAccounts

from .settings import MEDIA_ROOT, MEDIA_URL
from .views import index, user_login, user_logout, \
                    change_password, noaccess, success, \
                    OwnProfileUpdate, \
                    UsersList, \
                    UserProfileCreate, \
                    adm_index, \
                    UserProfilePersonDataUpdate, \
                    UserPermsFullUpdate
from .viewsajax import \
                    ajaxSelRowIndexToSession, \
                    ajaxStartRowIndexFromSession

urlpatterns = [
    # сайт: localhost або готовий сайт

    # /index/ та інші "кореневі" url - виклик з views.py проекту
    url(r'^$',          index,                          name='index0'),
    url(r'^index/$',    index,                          name='index'),
    url(r'^login/$',    user_login,                     name='login'),
    url(r'^logout/$',   user_logout,                    name='logout'),
    url(r'^noaccess/$', noaccess,                       name='noaccess'),
    url(r'^success/$',  success,                        name='success'),
    url(r'^register/$', UserProfileCreate.as_view(),    name='register'),

    # /own/profile/ та інші - дані залогіненого користувач (is_authenticated == True)
    url(r'^own/profile/$',          OwnProfileDetailShow.as_view(),name='own-profile'),
    url(r'^own/profile/update/$',   OwnProfileUpdate.as_view(),name='own-profile-update'),
    url(r'^own/change-password/$',  change_password,        name='change-password'),

    # /adm/ та інші - адміністративні сторінки (is_staff == True)
    url(r'^adm/index/$',                                adm_index,                      name='adm-index'),
    url(r'^adm/users/table/$',                          UsersTable.as_view(),            name='adm-users-list'),
    url(r'^adm/users/list/$',                           UsersList.as_view(),            name='adm-users-list'),
    # url(r'^adm/users/list/active/$',                    UsersListActive.as_view(),      name='adm-users-list'),
    # url(r'^adm/users/list/noactive/$',                  UsersListNoActive.as_view(),    name='adm-users-list'),
    url(r'^adm/users/(?P<pk>[0-9]+)/profile/$',         UserProfileDetailShow.as_view(),    name='all-users-detail'),
    url(r'^adm/users/(?P<pk>[0-9]+)/profile/update/$',  UserProfilePersonDataUpdate.as_view(),    name='all-users-detail'),
    # url(r'^adm/users/(?P<pk>[0-9]+)/permiss/$',         UserPermissDetail.as_view(),    name='all-users-detail'),
    url(r'^adm/users/(?P<pk>[0-9]+)/perms/update/$',  UserPermsFullUpdate.as_view(),    name='all-users-detail'),
    url(r'^adm/users/(?P<pk>[0-9]+)/perms/activate/$',UserPermsActivateUpdate.as_view(),  name='all-users-detail'),
    # url(r'^adm/users/(?P<pk>[0-9]+)/permiss/deactivate/$', UserPermissDeactivate.as_view(), name='all-users-detail'),

    # Виклик AJAX для koop_users_table
    url(r'^adm/users/ajax-activate-all-accounts$'  , AjaxActivateAllAccounts.as_view()),
    url(r'^adm/users/ajax-set-member-all-accounts$', AjaxSetMemberAllAccounts.as_view()),
    url(r'^adm/users/ajax-recognize-account$' , AjaxRecognizeAccount.as_view()),
    url(r'^adm/users/ajax-deny-account$'      , AjaxDenyAccount.as_view()),
    url(r'^adm/users/ajax-activate-account$'  , AjaxActivateAccount.as_view()),
    url(r'^adm/users/ajax-deactivate-account$', AjaxDeactivateAccount.as_view()),
    url(r'^adm/users/ajax-set-member-account$', AjaxSetMemberAccount.as_view()),
    url(r'^adm/users/ajax-deny-member-account$', AjaxDenyMemberAccount.as_view()),
    url(r'^adm/users/ajax-delete-account$'    , AjaxDeleteAccount.as_view()),

    # Виклик AJAX для обміну даними з сесією
    url(r'^ajax-selrowindex-to-session$',     ajaxSelRowIndexToSession),
    url(r'^ajax-startrowindex-from-session$', ajaxStartRowIndexFromSession),

    # /flats/ та інші - під'єднуємо urls.py аплікацій
    url(r'^flats/',     include('flats.urls')),
    url(r'^folders/',   include('folders.urls')),
    url(r'^lists/',     include('lists.urls')), # для прикладів з книги TDD with Python

    # /admin/ - під'єднання до вбудованого admin
    url(r'^admin/',     include(admin.site.urls)),
    # url(r'$',           index,              name='view_site'),

    # url(r'^register/$', Register.as_view(), name='register'),

]
urlpatterns += static.static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

# Друк списку всіх url.
# Закоментовано, тому що Pythonenywhere не сприйняв RegexURLResolver
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
class WalkURL():
    def __init__(self):
        self.all_url_names = []
        self.get_all_url_names()

    def url_walk(self, prefix, urlpatterns):
        for u in urlpatterns:
            if type(u) == RegexURLPattern:
                s = u.regex.pattern
                s = prefix + s.lstrip('^')
                print('%-50s %s' % (s, u.name))
                self.all_url_names.append((s, u.name))
            if type(u) == RegexURLResolver:
                self.url_walk(u.regex.pattern, u.url_patterns)
    def get_all_url_names(self):
        self.url_walk('^',urlpatterns)
        return self.all_url_names


# all_url = WalkURL().all_url_names
# print('all_url =', all_url)
