from django.conf.urls import patterns, url

from uks import views

urlpatterns = patterns('',
                       url(r'^project_list$', views.project_list, name='project_list'),
                       url(r'^project_create$', views.project_create, name='project_new'),
                       url(r'^project_update/(?P<pk>\d+)$', views.project_update, name='project_edit'),
                       url(r'^project_delete/(?P<pk>\d+)$', views.project_delete, name='project_delete'),
                       url(r'^project_view/(?P<pk>\d+)$', views.project_view, name='project_view'),
						
                       url(r'^issuetype_create/(?P<project_id>\d+)$', views.issuetype_create, name='issuetype_new'),
                       url(r'^issuetype_update/(?P<project_id>\d+)/(?P<issuetype_id>\d+)/$', views.issuetype_update, name='issuetype_edit'),
                       url(r'^issuetype_delete/(?P<project_id>\d+)/(?P<issuetype_id>\d+)/$', views.issuetype_delete, name='issuetype_delete'),
						
                       url(r'^priority_create/(?P<project_id>\d+)$', views.priority_create, name='priority_new'),
                       url(r'^priority_update/(?P<project_id>\d+)/(?P<priority_id>\d+)/$', views.priority_update, name='priority_edit'),
                       url(r'^priority_delete/(?P<project_id>\d+)/(?P<priority_id>\d+)/$', views.priority_delete, name='priority_delete'),
						
                       url(r'^status_create/(?P<project_id>\d+)$', views.status_create, name='status_new'),
                       url(r'^status_update/(?P<project_id>\d+)/(?P<status_id>\d+)/$', views.status_update, name='status_edit'),
                       url(r'^status_delete/(?P<project_id>\d+)/(?P<status_id>\d+)/$', views.status_delete, name='status_delete'),
						
                       url(r'^milestone_create/(?P<project_id>\d+)$', views.milestone_create, name='milestone_new'),
                       url(r'^milestone_update/(?P<project_id>\d+)/(?P<milestone_id>\d+)/$', views.milestone_update, name='milestone_edit'),
                       url(r'^milestone_delete/(?P<project_id>\d+)/(?P<milestone_id>\d+)/$', views.milestone_delete, name='milestone_delete'),
						
                       url(r'^issue_list$', views.issue_list, name='issue_list'),
                       url(r'^issue_create$', views.issue_create, name='issue_new'),
                       url(r'^issue_update/(?P<pk>\d+)$', views.issue_update, name='issue_edit'),
                       url(r'^issue_delete/(?P<pk>\d+)$', views.issue_delete, name='issue_delete'),
                       url(r'^issue_view/(?P<pk>\d+)$', views.issue_view, name='issue_view'),
						
                       url(r'^comment_list$', views.comment_list, name='comment_list'),
                       url(r'^comment_create$', views.comment_create, name='comment_new'),
                       url(r'^comment_update/(?P<pk>\d+)$', views.comment_update, name='comment_edit'),
                       url(r'^comment_delete/(?P<pk>\d+)$', views.comment_delete, name='comment_delete'),
						
                       url(r'^commit_list$', views.commit_list, name='commit_list'),
                       url(r'^commit_create$', views.commit_create, name='commit_new'),
                       url(r'^commit_update/(?P<pk>\d+)$', views.commit_update, name='commit_edit'),
                       url(r'^commit_delete/(?P<pk>\d+)$', views.commit_delete, name='commit_delete'),
						
)