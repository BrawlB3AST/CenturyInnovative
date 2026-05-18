from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('comment/<int:id>/', views.comment_post, name='comment_post'),
    path('search/suggestions/',     views.search_suggestions, name='search_suggestions'),
]