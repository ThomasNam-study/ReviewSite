from django.urls import path
from .views import search_move

urlpatterns = [
    path('', search_move, name="search"),
    path('<str:keyword>', search_move, name="search-result")
]