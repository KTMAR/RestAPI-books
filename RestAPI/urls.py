"""drfauthproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from RestAPI import settings
from books.views import BookListView, UserBookRelationView

router = SimpleRouter()

router.register(r'book', BookListView)
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('api/books/', include('books.urls')),
                  path('__debug__/', include('debug_toolbar.urls')),
                  path(('users/'), include('users.urls')),
                  path('password-reset/', PasswordResetView.as_view()),
                  path('password-reset-confirm/<slug:uidb64>/<slug:token>/',
                       PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
