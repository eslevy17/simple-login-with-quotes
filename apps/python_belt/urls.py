from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home),
    re_path(r'^create_user$', views.create_user),
    re_path(r'^login$', views.login),
    re_path(r'^logout$', views.logout),
    re_path(r'^board$', views.board),
    re_path(r'^add_quote$', views.add_quote),
    re_path(r'^user/(?P<number>\d+)$', views.user),
    re_path(r'^edit$', views.edit),
    re_path(r'^editing_user$', views.editing_user),
    re_path(r'^delete_quote/(?P<number>\d+)$', views.delete_quote),
    re_path(r'^like_quote/(?P<number>\d+)$', views.like_quote)

]
