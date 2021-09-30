from django.test import TestCase, Client
from restapi.models import Car, Rate
from django.urls import reverse
from .serializers import CarSerializer
from .views import CarViews


class CarTestCase(TestCase):
    def setUp(self):
        Car.objects.create(make="Nissan", model="Juke")
        Car.objects.create(make="Volkswagen", model="Golf")
        Car.objects.create(make="Dacia", model="Logan")

    def test_non_existent_cars(self):
        vw = Car.objects.get(make="Volkswagen")
        nis = Car.objects.get(make="Nissan")
        self.assertEqual(vw.model, 'Golf')
        self.assertEqual(nis.model, 'Juke')
        try:
            dac = Car.objects.get(make="Logan")
        except Car.DoesNotExist:
            dac = None
        self.assertEqual(dac, None)
        
    def test_cannot_post_duplicate_car(self):
        data_200 = {
            "make": "Honda",
            "model": "crosstour"
        }
        data_400 = {
            "make": "NiSaAn",
            "model": "JUkE"
        }
        response = self.client.post("/cars/", data=data_400)
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/cars/", data=data_200)
        self.assertEqual(response.status_code, 200)

    def test_case_sensitive_cars(self):
        data = {
            "make": "HOnDa",
            "model": "cRosStoUr"
        }

        response = self.client.post("/cars/", data=data)
        car = Car.objects.get(make=data['make'].lower().capitalize(), model = data['model'].lower().capitalize())
        self.assertEqual(car.make, "Honda")

    def test_car_delete(self):
        
        car = Car.objects.get(make='Nissan',model='Juke')
        test_response = self.client.delete('/cars/'+str(car.id))
        self.assertEqual(test_response.status_code, 200)

        null_response = self.client.delete('/cars/'+str(car.id))
        self.assertEqual(null_response.status_code, 404) 
    
class CarTestCase(TestCase):
    def setUp(self):
        car1 = Car(id = '1', make="Nissan", model="Juke",)
        car2 = Car(id = '2', make="Volkswagen", model="Golf")
        car3 = Car(id = '3', make="Honda", model="Crossover")
        car4 = Car(id = '4', make="Honda", model="FiT")
        rat1 = Rate(car_id=car1, rating=3)
        rat2 = Rate(car_id=car2, rating=4)
        rat3 = Rate(car_id=car3, rating=3)
        rat4 = Rate(car_id=car4, rating=1)

    
    def test_get_all_cars(self):
        # get API response
        client = Client()
        response = client.get(reverse('CarViews.post'))
        # get data from db
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
