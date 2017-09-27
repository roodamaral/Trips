from django.conf.urls import url, include
from django.contrib import admin
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login), 
    url(r'^logoff$', views.logoff),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^addtrip$', views.addtrip),
    url(r'^travels/destination/(?P<id>\d+)$', views.showtrip),
    url(r'^join$', views.join)
    ]
