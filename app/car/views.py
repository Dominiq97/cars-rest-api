from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from core.models import Car
from .serializers import CarSerializer, PopularSerializer
from core.models import Rate, Car

from car import serializers

class CarsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Car.objects.all()
    serializer_class = serializers.CarSerializer

class CarViews(APIView):

    def get(self, request, id=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        car = get_object_or_404(Car, id=id)
        car.delete()
        return Response({"status": "success", "data": "Car Deleted"})

class PopularView(APIView):
    def get(self, request):
        cars = Car.objects.order_by('-rates_number')
        serializer = PopularSerializer(cars, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
