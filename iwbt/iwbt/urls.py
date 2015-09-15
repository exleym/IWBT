"""iwbt URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
import iwbt.views as main_views

urlpatterns = [
    url(r'^$', main_views.home),
    url(r'^about_us/$', main_views.about_us),
    url(r'^time/$', main_views.current_datetime),
    url(r'^select_river/$', main_views.select_river),
    url(r'^river/(?P<river_name>[A-z]+)/(?P<section_name>[A-z0-9_]+)/$', main_views.show_river),
    #url(r'^river/(?P<river_name>[A-z]+)/(?P<section_name>[A-z0-9]', main_views.show_river),
    url(r'^admin/', include(admin.site.urls)),
]
