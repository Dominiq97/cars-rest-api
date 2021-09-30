from rest_framework import serializers
from restapi.models import Car, Rate, CarManager
import requests,json


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','make', 'model','avg_rating']

    def validate(self, attrs):
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/'+attrs['make']+'?format=json'
        r = requests.get(url)
        response_data = json.loads(r.text)
        result = response_data.get('Results')
        c = False
        lower_str2 = attrs['model'].lower()
        for i in result:
            lower_str1 = i['Model_Name'].lower()
            if lower_str1==lower_str2:
                c = True
        cars_dup = Car.objects.filter(make=attrs['make'].lower().capitalize(),model=attrs['model'].lower().capitalize())
        if c == False or len(result)==0:
            raise serializers.ValidationError('Wrong Make or Model!')
        if len(cars_dup)>1:
            raise serializers.ValidationError('Duplication Error!')
        attrs['make'] = attrs['make'].lower().capitalize()
        attrs['model'] = attrs['model'].lower().capitalize()
        return attrs

class CarPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id','make', 'model')

    def create(self, validated_data):
        return CarManager.create_car(**validated_data)

class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id','make', 'model','rates_number')