from django.urls import path
from car import views 
from .views import CarViews
 
urlpatterns = [
    path('cars/', CarViews.as_view()),
    path('cars/<int:id>', CarViews.as_view())
]
