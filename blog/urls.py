from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import (ShowUsersListView, ShowUserDetailView, ShowPostDetailView, ChangePostView,
                    CreateNewPostView, ShowListPostsView, ShowCertainUserPosts, CustomLoginView)

urlpatterns = [
    url(r'^create/', CreateNewPostView.as_view(), name='new_post'),
    url(r'^users/(?P<pk>[0-9]+)/$', ShowCertainUserPosts.as_view(), name='user_posts'),
    url(r'^users/', ShowUsersListView.as_view(), name='users_list'),
    url(r'^(?P<pk>[0-9]+)/$', ShowPostDetailView.as_view(), name='post_detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', ChangePostView.as_view(), name='update_post'),
    url(r'login/', CustomLoginView.as_view(), name='login'),
    url(r'^$', ShowListPostsView.as_view(), name='posts'),
]