from django.urls import path
from . import views

urlpatterns = [
    # Post CRUD
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit/', views.post_update, name='post_update'),
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),

    # Categories and Tags
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),

    # Comments
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
