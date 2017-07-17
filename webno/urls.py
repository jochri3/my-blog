from django.conf.urls import url
from webno import views
from .feeds import LatestPostsFeed

urlpatterns = [
    url(r'^$',views.list,name='list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.list,name='post_list_by_tag'),
    url(r'^post=(?P<id>[0-9]{1,3})$',views.detail,name='detail'),
    url(r'^create$',views.create,name='create'),
    url(r'^edit/(?P<id>[0-9]{1,3})$',views.edit,name='edit'),
    url(r'^delete/(?P<id>[0-9]{1,3})$',views.delete,name='delete'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    url(r'^search/$', views.post_search, name='post_search'),
]