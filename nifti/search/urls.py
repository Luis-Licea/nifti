# Import path for matching url patters to views.
from django.urls import path, include
# Import views.py from local directory.
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.search, name='search-home'),
  path('s/', views.SearchListView.as_view(), name='search-page'),
  path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
  path('post/new/', views.PostCreateView.as_view(), name='post-create'),
  path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
  path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]