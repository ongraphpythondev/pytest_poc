import pytest
from django.urls import reverse
# from django.contrib.auth import user



# Create your tests here.

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.mark.django_db
def test_registration_succes(api_client , django_user_model):
    url = reverse('registration')
    response = api_client.post(url , {"username":"ritesh", "email":"riteshpandey1200@gmail.com","password":"pandey1200"})
    assert django_user_model.objects.count() == 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_error(api_client ):
    url = reverse('registration')
    response = api_client.post(url )
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_succes(api_client , django_user_model):
    url = reverse('registration')
    response = api_client.post(url , {"username":"ritesh", "email":"riteshpandey1200@gmail.com" , "password":"pandey1200"})

    
    url = reverse('login')
    response = api_client.post(url , {"username":"ritesh" , "password":"pandey1200"})

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_error(api_client , django_user_model):
    url = reverse('registration')
    response = api_client.post(url , {"username":"ritesh", "email":"riteshpandey1200@gmail.com" , "password":"pandey1200"})

    
    url = reverse('login')
    response = api_client.post(url )

    assert response.status_code == 404


@pytest.mark.django_db
def test_login_anomymoususer(api_client , django_user_model):
    url = reverse('registration')
    response = api_client.post(url , {"username":"ritesh", "email":"riteshpandey1200@gmail.com" , "password":"pandey1200"})

    from django.contrib import auth
    user = auth.get_user(api_client) # it returns User or AnonymousUser

    url = reverse('login' )
    response = api_client.post(url , {"username":"ritesh" , "password":"pandey1200"})
    url = reverse('login')
    response = api_client.post(url , {"username":"ritesh" , "password":"pandey1200"})

    assert response.status_code == 400
    
