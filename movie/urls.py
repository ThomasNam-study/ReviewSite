from django.urls import path
from .views import search_move

urlpatterns = [
    path('', search_move, name="search")
]