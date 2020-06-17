from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("author/", views.AuthorView.as_view(), name="author-list"),
    path("author/<str:slug>/", views.AuthorManageView.as_view(), name="author-detail"),
    path(
        "social_account/", views.SocialAccountView.as_view(), name="social_account-list"
    ),
    path(
        "social_account/<str:slug>/",
        views.SocialAccountManageView.as_view(),
        name="social_account-detail",
    ),
    path("tag/", views.TagView.as_view(), name="tag-list"),
    path("tag/<str:slug>/", views.TagManageView.as_view(), name="tag-detail"),
    path("category/", views.CategoryView.as_view(), name="category-list"),
    path(
        "category/<str:slug>/",
        views.CategoryManageView.as_view(),
        name="category-detail",
    ),
    path("post/", views.PostView.as_view(), name="post-list"),
    path("post/<str:slug>/", views.PostManageView.as_view(), name="post-detail"),
]
