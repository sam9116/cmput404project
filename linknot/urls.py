"""
Definition of urls for linknot.
"""

from django.conf.urls import include
from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib import admin
admin.autodiscover()

import main.forms
import main.views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', main.views.linknothome, name='home'),


    # url(r'^linknot/', include('linknot.linknot.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md


    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',main.views.login_user, name='login'),
    url(r'^logout$',django.contrib.auth.views.logout,{'next_page': '/',},name='logout'),




    #url(r'^author/posts',main.views.postViewSet.myposts,name="myposts"),
    #url(r'^author/(?P<author_id>[^/]+)/posts',main.views.author,name="somebody's post"),
    url(r'^author/(?P<pk1>[0-9a-f-]+)/friends/(?P<pk2>[0-9a-f-]+)',main.views.friends.as_view(),name="check friends"),
    
    
    
    
    
    
    url(r'^author/(?P<pk>[0-9a-f-]+)/friends$',main.views.friendlist.as_view(),name="my friends"),




    url(r'^posts/$',main.views.Listposts.as_view(),name="myposts"),
    url(r'^posts/(?P<pk>[0-9a-f-]+)/$',main.views.singlepost.as_view(),name="singlepost"),
    #url(r'^posts/(?P<post_id>[^/]+)/comment',main.views.comments,name="commentsection"),

    #url(r'^friendrequest',main.views.friendrequest,name="make friends"),




]
