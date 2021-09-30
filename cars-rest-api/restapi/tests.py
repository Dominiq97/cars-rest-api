from django.test import TestCase, Client
from restapi.models import Car, Rate
from django.urls import reverse, resolve
from .serializers import CarSerializer, PopularSerializer
from .views import CarViews
from rest_framework.test import APITestCase
import random

########### Urls tests 

class UrlsTestCase(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(make="Nissan", model="Juke",rates_number="5")

    def test_get_cars_url(self):
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)

    def test_get_populars_url(self):
        response = self.client.get(reverse('popular'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_rates_url(self):
        response = self.client.get('/rate/')
        self.assertEqual(response.status_code, 200)

    def test_post_rates_url(self):
        payload = {
            'car_id' : self.car1.id,
            'rating' : 4
        }
        response = self.client.post('/rate/', payload)
        self.assertEqual(response.status_code, 200)

    def test_post_cars_url(self):
        data = {
            "make": "Honda",
            "model": "Crosstour"
        }
        response = self.client.post('/cars/', data)
        self.assertEqual(response.status_code, 200)

class CarTestCase(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(make="Nissan", model="Juke",rates_number="5")
        self.car2 = Car.objects.create(make="Volkswagen", model="Golf",rates_number="7")
        self.car3 = Car.objects.create(make="BMW", model="X2",rates_number="3")
        self.car4 = Car.objects.create(make="Fiat", model="500",rates_number="8")
        self.cars = []
        self.cars.append(self.car1)
        self.cars.append(self.car2)
        self.cars.append(self.car3)
        self.cars.append(self.car4)

######### Get/ cars tests

    def test_non_existent_cars(self):
        self.assertEqual(self.car2.model, 'Golf')
        self.assertEqual(self.car1.model, 'Juke')
        payload = {
            "make":"Dacia",
            "model":"Logan"
        }
        response = self.client.post("/cars/", data=payload)
        self.assertEqual(400,response.status_code)


    def test_resolution_for_cars(self):
        resolver = resolve('/cars/')
        self.assertEqual(resolver.func.cls, CarViews)

    def test_can_browse_all_cars(self):
        response = self.client.get(reverse("cars"),args=[''])

        self.assertEquals(200, response.status_code)
        self.assertEquals(len(self.cars), len(response.data['data']))

        for car in self.cars:
            self.assertIn(CarSerializer(instance=car).data,response.data['data'])

######### POST/ cars tests

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

######### DELETE/ cars tests

    def test_car_delete(self):
        test_response = self.client.delete('/cars/'+str(self.car1.id))
        self.assertEqual(test_response.status_code, 200)

        null_response = self.client.delete('/cars/'+str(self.car1.id))
        self.assertEqual(null_response.status_code, 404) 

        error_response = self.client.delete('/cars/'+"h9r")
        self.assertEqual(error_response.status_code, 404) 

######### GET/ popular tests

    def test_get_popular_cars(self):
        response = self.client.get('/popular/')
        self.assertEquals(len(self.cars), len(response.data['data']))

        for car in self.cars:
            self.assertIn(PopularSerializer(instance=car).data,response.data['data'])

    def test_get_correct_popular(self):
        response = self.client.get(reverse("popular"),args=[''])

        self.assertEquals(200, response.status_code)
        self.assertEquals(len(self.cars), len(response.data['data']))
        max = 0
        for car in self.cars:
            if int(car.rates_number)>max:
                max = int(car.rates_number)
            self.assertIn(PopularSerializer(instance=car).data,response.data['data'])
        max_resp = 0
        for i in response.data['data']:
            if i['rates_number'] > max_resp:
                max_resp = i['rates_number']
        self.assertEquals(max,max_resp)
        
    def test_correct_order_popular(self):
        response = self.client.get(reverse("popular"),args=[''])
        correct = True
        current_max = response.data['data'][0]['rates_number']
        for i in response.data['data']:
            if i['rates_number'] > current_max:
                correct = False
                break
            else:
                current_max = i['rates_number']
                
        self.assertTrue(correct)

######### POST/ rate tests
        
class RateTestCase(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(make="Nissan", model="Juke",rates_number="5")

    def test_avg_rating_car(self):
        randlist = []
        for i in range(1,random.randint(2, 10)): 
            n = random.randint(1,5)
            randlist.append(n)

        actual_avg ="{:.1f}".format(sum(randlist) / len(randlist)) 
        rates = {}
        for j in range(len(randlist)):
            rates['car_id'] = self.car1.id
            rates['rating'] = randlist[j]
            response = self.client.post("/rate/",rates)
            self.assertEqual(response.status_code,200)
            rates = {}

        respget = self.client.get("/cars/")
        avg = respget.data['data'][0]['avg_rating']
        self.assertEqual(avg,float(actual_avg))

    def test_not_lower_higher(self):
        payload = {
            'car_id' : self.car1.id,
            'rating' : 8
        }
        response = self.client.post("/rate/",payload)
        self.assertEqual(response.status_code,400)
        payload = {
            'car_id' : self.car1.id,
            'rating' : 0
        }
        response = self.client.post("/rate/",payload)
        self.assertEqual(response.status_code,400)
        payload = {
            'car_id' : self.car1.id,
            'rating' : -4
        }
        response = self.client.post("/rate/",payload)
        self.assertEqual(response.status_code,400)
        payload = {
            'car_id' : self.car1.id,
            'rating' : 'd'
        }
        response = self.client.post("/rate/",payload)
        self.assertEqual(response.status_code,400)
        payload = {
            'car_id' : self.car1.id,
            'rating' : 3
        }
        response = self.client.post("/rate/",payload)
        self.assertEqual(response.status_code,200)
        response = self.client.post("/rate/",payload)
