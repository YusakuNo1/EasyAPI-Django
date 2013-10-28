from django.conf.urls import patterns, include, url
from django.contrib import admin
from easyapi import views


# Admin
admin.autodiscover()


urlpatterns = patterns('',
    # EasyAPI
 	url(r'^$', views.ApiRoot.as_view(), name='api-root'),
	
    url(r'^forum_posts/$', views.ForumPostList.as_view(), name='forumPost-list'),
    url(r'^forum_posts/(?P<pk>[0-9]+)/$', views.ForumPostDetail.as_view(), name='forumPost-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/create/$', views.UserCreate.as_view(), name='user-create'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
	
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Testing
    url(r'^userLoginTest', views.UserLoginTest, name='user-login-test'),
)
