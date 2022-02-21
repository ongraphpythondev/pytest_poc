import pytest
from django.urls import reverse
from django.contrib.auth.hashers import check_password


# Create your tests here.

# NOTE :  To print while testing we have to type pytest -rP


@pytest.mark.django_db
def test_registration_succes(api_client, django_user_model):
    url = reverse("registration")
    response = api_client.post(
        url,
        {
            "username": "ritesh",
            "email": "riteshpandey1200@gmail.com",
            "password": "pandey1200",
        },
    )
    assert django_user_model.objects.count() == 1
    assert django_user_model.objects.all()[0].username == "ritesh"
    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_error(api_client, django_user_model):
    url = reverse("registration")
    response = api_client.post(url)
    assert django_user_model.objects.count() == 0
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_succes(api_client, create_user, login_user):

    assert login_user.status_code == 200


@pytest.mark.django_db
def test_login_error(api_client):
    url = reverse("login")
    response = api_client.post(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_login_anomymoususer(api_client, create_user, login_user):

    url = reverse("login")
    response = api_client.post(url, {"username": "ritesh", "password": "pandey1200"})

    assert response.status_code == 401


@pytest.mark.django_db
def test_logout_success(api_client, create_user, login_user):

    url = reverse("auth_logout")
    response = api_client.get(url)

    assert response.status_code == 200


class TestChangePassword:
    @pytest.mark.django_db
    def test_change_password_user_not_found(self, api_client, create_user, login_user):

        url = reverse("auth_change_password", args=[2])
        data = {
            "old_password": "pandey1200",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_change_password_user_not_login_with_correct_account(
        self, api_client, create_user, login_user, django_user_model
    ):

        django_user_model.objects.create_user(
            username="manish", email="manishpandey1200@gmail.com", password="pandey1200"
        )

        url = reverse("auth_change_password", args=[create_user.objects.all()[1].pk])
        data = {
            "old_password": "pandey1200",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_change_password_user_password_not_correct(
        self, api_client, create_user, login_user
    ):

        url = reverse("auth_change_password", args=[create_user.objects.all()[0].pk])
        data = {
            "old_password": "pandey1202",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_change_password_pass1_and_pass2_incorrect(
        self, api_client, create_user, login_user
    ):

        url = reverse("auth_change_password", args=[create_user.objects.all()[0].pk])
        data = {
            "old_password": "pandey1200",
            "password": "pandey1201",
            "password2": "pandey12012",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_change_password_correct(self, api_client, create_user, login_user):

        url = reverse("auth_change_password", args=[create_user.objects.all()[0].pk])
        data = {
            "old_password": "pandey1200",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert check_password("pandey1201", create_user.objects.all()[0].password)
        assert response.status_code == 202


class TestResetPassword:
    @pytest.mark.django_db
    def test_reset_password_user_not_found(self, api_client, create_user):

        url = reverse("auth_reset_password")
        data = {
            "username": "manish",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_reset_password_pass1_and_pass2_incorrect(self, api_client, create_user):

        url = reverse("auth_reset_password")
        data = {
            "username": "ritesh",
            "password": "pandey1201",
            "password2": "pandey12012",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_change_password_correct(self, api_client, create_user):

        url = reverse("auth_reset_password")
        data = {
            "username": "ritesh",
            "password": "pandey1201",
            "password2": "pandey1201",
        }
        response = api_client.post(url, data)
        assert check_password("pandey1201", create_user.objects.all()[0].password)
        assert response.status_code == 202
