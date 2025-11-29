from django.urls import path
from . import views   

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tag/<int:pk>/", views.TagPostsView.as_view(), name="tag-posts"),
    path("category/<int:pk>/", views.CategoryPostsView.as_view(), name="category-posts"),
    
]