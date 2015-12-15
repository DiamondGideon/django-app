from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_home, name='post_home'),
    url(r'^posts/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/makebet/$', views.post_make_bet, name='post_make_bet'),
    url(r'^post/(?P<pk>[0-9]+)/set_race_result/$', views.post_result_and_delete, name='post_result_and_delete'),
    url(r'^post/(?P<pk>[0-9]+)/raceresult/$', views.show_result, name='show_result'),
]