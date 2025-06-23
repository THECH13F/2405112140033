from django.urls import path
from .views import CRShortUrlsAPIView,RedShortUrlsAPIView

urlpatterns = [
    path('create/', CRShortUrlsAPIView.as_view(), name='create-shortlink'),
    path('<str:code>/', RedShortUrlsAPIView.as_view(), name='redirect-shortlink'),
]