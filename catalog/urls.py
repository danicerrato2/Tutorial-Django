from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<str:slug>', views.BookDetailView.as_view(), name='book-detail'),
    path('search/', views.SearchView.as_view(), name='search'),
]
