from django.conf.urls import url
from firstapp import views

urlpatterns = [
    url(r'^login/$', views.page_login, name='login'),
    url(r'^logout/$', views.page_logout, name='logout'),
    url(r'changepassword/$', views.page_change_password, name="changepassword"),
    url(r'^registration/$', views.page_registration, name='registration'),
    url(r'^tourpage/(?P<name>\D+)/', views.page_tours, name="tourpage"),
    url(r'^userpage/$', views.page_user, name="userpage"),
    url(r'^$', views.page_tour_instance, name='main'),
    url(r'^aboutus/$', views.page_about_us, name="aboutus"),
    url(r'^confirmation/(?P<name>[-\w]+)/', views.page_confirmation, name="confirmation")]
