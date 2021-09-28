from django.urls import path
from .views import RateViews
from rate import views 
 
urlpatterns = [
    path('rate/', RateViews.as_view()),
]
