from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'hotel_auto'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    url(r'^inputs/$', views.inputs, name='inputs'),
    url(r'^movement/$', views.movement, name='movement'),
    url(r'^no_movement/$', views.no_movement, name='no_movement'),

]