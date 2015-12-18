# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('dfss.demo.views',
                       url(r'^resumes/$', 'resumes', name='resumes'),
                       url(r'^resume/(?P<epoc_time>[0-9]+)/$', 'get_resume', name='resume'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^login/$', 'user_login', name='login'),
                       url(r'^logout/$', 'user_logout', name='logout'),
                       url(r'^$', RedirectView.as_view(url='/demo/resumes/')),
                       )
