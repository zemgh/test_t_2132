from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'books', views.BookViewSet, basename='books')
router.register(r'authors', views.AuthorViewSet, basename='authors')


urlpatterns = [
    path('', include(router.urls))
]