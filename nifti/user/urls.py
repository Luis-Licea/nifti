# Import path for matching url patters to views.
from django.urls import path, include
# Import views.py from local directory.
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('<str:username>/', views.profile_detail, name='user-static-profile'),
]
