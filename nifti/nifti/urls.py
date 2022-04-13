"""nifti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Import include function so that we can include urls defined in another app,
# thus increasing modularity.
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views
from user import views as user_views


urlpatterns = [
    path('', home_views.home, name='home-home'),
    path('login', auth_views.LoginView.as_view(template_name='home/login.html'), name='home-login'),
    path(
        'logout',
        auth_views.LogoutView.as_view(template_name='home/logout.html'),
        name='home-logout'
    ),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('profile', user_views.profile, name='user-profile'),
    path('user/', include('user.urls')),
    path('register', home_views.register, name='home-register'),
    path('unregister', user_views.deleteuser, name='home-unregister'),
    path('about', home_views.about, name='home-about'),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
]

#if in debug/development mode, add these URLs
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
