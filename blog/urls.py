from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('comment/<int:id>/', views.comment_post, name='comment_post'),
    path('search/suggestions/',     views.search_suggestions, name='search_suggestions'),
]

postgresql://socialuser:gmTLzZL04UFyFvHbnojrCsl7EMDOilbA@dpg-d8j7v8uk1jcs73f31p6g-a.singapore-postgres.render.com/socialdb_llsq