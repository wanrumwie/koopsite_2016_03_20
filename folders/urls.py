from django.conf.urls import url
from folders.views import folderDownload, ReportPreview
from koopsite.views import page_not_ready
from .views import success, \
                    FolderCreate, \
                    FolderCreateInFolder, \
                    FolderUpdate, \
                    FolderDelete, \
                    FolderList, \
                    FolderDetail, \
                    ReportUpload, \
                    ReportUploadInFolder, \
                    ReportUpdate, \
                    ReportDelete, \
                    ReportList, \
                    ReportDetail, \
                    reportDownload, \
                    FolderParentList
from .viewsajaxfolder import \
                    FolderContents, \
                    ajaxFoldersTreeFromBase, \
                    AjaxFolderCreate, \
                    AjaxFolderRename, \
                    AjaxFolderDelete, \
                    XHRFolderDownload, \
                    XHRReportUpload, \
                    AjaxReportRename, \
                    AjaxReportDelete, \
                    XHRReportDownload, \
                    AjaxElementMove

"""
/folders/ - під'єднано у модулі koopsite.urls.py:
            url(r'^folders/',   include('folders.urls')),
"""

urlpatterns = [
    url(r'^create/$',       FolderCreate.as_view(), name='folder-create'),
    url(r'^success/$',      success,                name='success'),
    url(r'^list/$',         FolderList.as_view(),   name='folder-list'),

    url(r'^(?P<pk>[0-9]+)/$', FolderDetail.as_view(), name='folder-detail'),
    url(r'^(?P<pk>[0-9]+)/page(?P<page>\d+)/$',
                            FolderDetail.as_view(), name='folder-detail-page'),
    url(r'^(?P<pk>[0-9]+)/update/$', FolderUpdate.as_view(), name='folder-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', FolderDelete.as_view(), name='folder-delete'),
    url(r'^(?P<pk>[0-9]+)/download/$', folderDownload, name='folder-download'),

    url(r'^(?P<parent>\d+)/create/$',
                    FolderCreateInFolder.as_view(), name='folder-create-in'),
    url(r'^(?P<parent>\d+)/report/upload/$',
                     ReportUploadInFolder.as_view(), name='report-upload-in'),

    url(r'^report/upload/$', ReportUpload.as_view(), name='report-upload'),
    url(r'^report/list/$',   ReportList.as_view(),   name='report-list'),
    url(r'^report/(?P<pk>[0-9]+)/$', ReportDetail.as_view(), name='report-detail'),
    url(r'^report/(?P<pk>[0-9]+)/preview/$', ReportPreview.as_view(), name='report-preview'),
    url(r'^report/(?P<pk>[0-9]+)/page(?P<page>\d+)/$',
                        ReportDetail.as_view(), name='report-detail-page'),
    url(r'^report/(?P<pk>[0-9]+)/update/$', ReportUpdate.as_view(), name='report-update'),
    url(r'^report/(?P<pk>[0-9]+)/download/$', reportDownload, name='report-download'),
    url(r'^report/(?P<pk>[0-9]+)/delete/$', ReportDelete.as_view(), name='report-delete'),

    url(r'^parents/$', FolderParentList.as_view(), name='folder-parents'),
    url(r'^(?P<pk>[0-9]+)/contents/$',
                FolderContents.as_view(), name='folder-contents'),

    url(r'^ajax-folders-tree-from-base$',     ajaxFoldersTreeFromBase),
    url(r'^ajax-folder-create$'  , AjaxFolderCreate.as_view()),
    url(r'^ajax-folder-rename$'  , AjaxFolderRename.as_view()),
    url(r'^ajax-folder-delete$'  , AjaxFolderDelete.as_view()),
    url(r'^ajax-report-rename$'  , AjaxReportRename.as_view()),
    url(r'^ajax-report-delete$'  , AjaxReportDelete.as_view()),
    url(r'^ajax-element-move$'  ,  AjaxElementMove.as_view()),
    url(r'^ajax-folder-download$', XHRFolderDownload.as_view()),
    url(r'^ajax-report-download$', XHRReportDownload.as_view()),
    url(r'^ajax-report-upload$'  , XHRReportUpload.as_view()),

]

# urlpatterns += staticfiles_urlpatterns()
'''
# from Tango with Django:
if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
'''
