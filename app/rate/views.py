from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import RateSerializer
from core.models import Rate, Car
from rate import serializers

class RateViews(APIView):

    def get(self, request, id=None):
        rates = Rate.objects.all()
        serializer = RateSerializer(rates, many=True)
        return Response({ "rates": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            car = Car.objects.get(id = request.data['car_id'])
            query = Rate.objects.filter(car_id = car.id)
            sum = 0
            for i in query:
                sum+=i.rating
            val = ("{:.1f}".format(sum/len(query)))
            car.avg_rating = val
            car.no_rating = car.no_rating + 1
            car.save(update_fields=['avg_rating','no_rating'])
            return Response({ "rates": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({ "rates": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
