from django.urls import path, include

from . import views

from .views import main_page, article_create, article_edit, article_delete

# from .views import ArticleViewSet

# from rest_framework.routers import DefaultRouter

from django.conf import settings

from django.conf.urls.static import static

from django.contrib import admin

# router = DefaultRouter()

# router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', main_page, name='main_page'),
    # path('api/', include(router.urls)),

    path('article/create/', article_create, name='article_create'),
    path('article/<int:pk>/edit/', article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', article_delete, name='article_delete'),
    path('article/<int:article_id>/like/', views.toggle_like, name='article_like'),
    
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),

    path('announcements/', views.announcements_list, name='announcements'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)