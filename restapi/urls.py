from django.urls import path
from .views import CarViews, PopularView, RateViews
 
urlpatterns = [
    path('cars/', CarViews.as_view()),
    path('cars/<int:id>', CarViews.as_view()),
    path('popular/', PopularView.as_view()),
    path('rate/', RateViews.as_view()),
]