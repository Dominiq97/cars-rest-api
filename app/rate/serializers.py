from django.core.checks.messages import ERROR
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import Rate, Car
from core import models
import requests,json;
from django.http import JsonResponse

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')

  


