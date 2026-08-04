from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [

    path('',                        views.home,             name='home'),
    path('posts/',                  views.posts,            name='posts'),
    path('post/<int:id>/',          views.post_detail,      name='post_detail'),
    path('create/',                 views.create_post,      name='create_post'),
    path('edit/<int:id>/',          views.edit_post,        name='edit_post'),
    path('delete/<int:id>/',        views.delete_post,      name='delete_post'),

    # auth
    path('signup/',                 views.signup_view,      name='signup'),
    path('login/',                  views.login_view,       name='login'),
    path('logout/',                 views.logout_view,      name='logout'),

    # profiles
    path('author/<str:username>/',  views.author_profile,   name='author_profile'),
    path('profile/edit/',           views.edit_profile,     name='edit_profile'),

    # admin
    path('admin-dashboard/',        views.admin_dashboard,  name='admin_dashboard'),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

