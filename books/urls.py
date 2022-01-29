from django.conf.urls.static import static
from django.urls import path

from RestAPI import settings
from .views import BookList, BookDetail

urlpatterns = [
                  path('', BookList.as_view()),
                  path('<int:pk>/', BookDetail.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
