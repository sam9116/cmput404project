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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',main.views.login_user, name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

]
