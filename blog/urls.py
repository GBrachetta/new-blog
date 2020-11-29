from django.urls import path
from .views import (
    PostListView,
    about,
    # PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    home,
    post_detail,
    # add_comment_to_post,
)

urlpatterns = [
    path("", home, name="home"),
    path("blog/", PostListView.as_view(), name="blog-home"),
    path(
        "user/<str:username>/", UserPostListView.as_view(), name="user-posts"
    ),
    # path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/", post_detail, name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path(
        "post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"
    ),
    path(
        "post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"
    ),
    path("about/", about, name="blog-about"),
    # path("post/<int:pk>/comment", add_comment_to_post, name="add-comment"),
]
