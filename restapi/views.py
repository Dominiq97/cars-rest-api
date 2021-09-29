from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import RateSerializer, CarPostSerializer, CarPostSerializer, CarSerializer, PopularSerializer
from restapi.models import Car, Rate

class RateViews(APIView):

    def get(self, request, id=None):
        rates = Rate.objects.all()
        serializer = RateSerializer(rates, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


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
            car.rates_number = car.rates_number + 1
            car.save(update_fields=['avg_rating','rates_number'])
            return Response({ "rates": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({ "rates": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CarsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

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



