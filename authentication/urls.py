from django.urls import path
from . import views
import django.contrib.auth.urls as urls

urlpatterns = [
   path('signup/', views.signup, name='signup'),
]