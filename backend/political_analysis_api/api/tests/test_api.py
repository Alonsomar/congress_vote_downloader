from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_list_diputados(self):
        response = self.client.get(reverse('diputados-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_proyecto_not_found(self):
        response = self.client.get(reverse('proyecto-detail', args=['boletin_que_no_existe']))
        self.assertEqual(response.status_code, 404)
