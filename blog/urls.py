from django.urls import path

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog-delete'),

]
