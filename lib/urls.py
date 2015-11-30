from django.conf.urls import patterns, include, url
from django.contrib import admin
from lib.view import search, search_result, detail

urlpatterns = patterns('',
    (r'^search/', search),
    (r'^result/$', search_result),
    (r'^result/(\d+)$', detail)
)
