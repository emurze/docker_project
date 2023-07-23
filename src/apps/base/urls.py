from django.shortcuts import redirect
from django.urls import path

from .views import PostList, Share, PostDetail

app_name = 'base'

urlpatterns = [
    path('', lambda _: redirect('base:list')),
    path('list/', PostList.as_view(), name='list'),
    path('list/<slug:tag_slug>', PostList.as_view(), name='list_slug'),

    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         PostDetail.as_view(), name='detail'),
    path('share/<int:pk>/', Share.as_view(), name='share'),
]
