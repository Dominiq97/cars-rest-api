from django.urls import path
from .views import CarViews, PopularView, RateViews
 
urlpatterns = [
    path('cars/', CarViews.as_view(),name='cars'),
    path('cars/<int:id>', CarViews.as_view(), name='car-post'),
    path('popular/', PopularView.as_view(), name='popular'),
    path('rate/', RateViews.as_view(),name='rate-post'),
]