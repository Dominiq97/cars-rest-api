from rest_framework import serializers
from core.models import Rate

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')

  


