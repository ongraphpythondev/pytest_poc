import pytest
from django.urls import reverse


@pytest.fixture()
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

   
@pytest.fixture()
def create_user(django_user_model):
   django_user_model.objects.create_user(username="ritesh", email="riteshpandey1200@gmail.com" , password="pandey1200")

   return django_user_model

   
@pytest.fixture()
def login_user(api_client):
   url = reverse('login' )
   response  = api_client.post(url , {"username":"ritesh" , "password":"pandey1200"})

   return response