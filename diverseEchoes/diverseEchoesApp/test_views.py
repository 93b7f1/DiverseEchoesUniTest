import json
import unittest
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock, Mock
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from diverseEchoesApp import views
from diverseEchoesApp.models import UserProfile, Comment, Echo
from diverseEchoesApp.serializers import ComentarioSerializer
from diverseEchoesApp.views import EchoViewSet, CommentViewSet, EchoCommentsViewSet, EchoViewSetLastFive

#Comandos para rodar os teste
#python manage.py test diverseEchoesApp.test_views
#coverage run manage.py test diverseEchoesApp.test_views
#coverage report
#coverage html

#Use "coverage erase" para apagar a cobertura e repita os passos acima para refazer

class EchoViewSetTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.echo_url = reverse("echo", args=[1])

    @patch('diverseEchoesApp.views.EchoesAPIView.queryset')
    def test_list_echoes(self, mock_queryset):

        echo_mock = {
            "id": 1,
            "echolink": "echolink1",
            "url": "url1",
            "genero": "genero1",
            "visualizacao": 0,
            "pixiv": "pixiv1",
            "tipo": "tipo",
            "comments": [],
            "user": 1
        }

        mock_queryset.all.return_value = [echo_mock]

        response = self.client.get(self.echo_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), echo_mock)



class CustomLoginViewTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")

    @patch('diverseEchoesApp.views.UserProfile.objects.get')
    @patch('diverseEchoesApp.views.check_password')
    def test_login_successful(self, mock_check_password, mock_user_profile_get):
        mock_user_profile = self.create_mock_user_profile("usuario_teste", "senha_teste")
        mock_user_profile_get.return_value = mock_user_profile
        mock_check_password.return_value = True
        data = {
            "username": "usuario_teste",
            "password": "senha_teste",
        }

        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Login bem-sucedido')

    @patch('diverseEchoesApp.views.UserProfile.objects.get')
    @patch('diverseEchoesApp.views.check_password')
    def test_login_invalid_credentials(self, mock_check_password, mock_user_profile_get):
        mock_user_profile = self.create_mock_user_profile("usuario_teste", "senha_teste")
        mock_user_profile_get.return_value = mock_user_profile
        mock_check_password.return_value = False

        data = {
            "username": "usuario_teste",
            "password": "senha_incorreta",
        }

        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error'], 'Credenciais inválidas')

    @patch('diverseEchoesApp.views.UserProfile.objects.get')
    def test_login_user_not_found(self, mock_user_profile_get):
        mock_user_profile_get.side_effect = UserProfile.DoesNotExist

        data = {
            "username": "usuario_inexistente",
            "password": "senha_qualquer",
        }

        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Usuário não encontrado')

    def create_mock_user_profile(self, username, password):
        return UserProfile(username=username, password=password)


class EchoViewSetLastFiveTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EchoViewSetLastFive.as_view({'get': 'last'})

    @patch('diverseEchoesApp.views.Echo.objects')
    def test_last_five_echoes(self, mock_echo_objects):
        echoes = [Mock(id=i) for i in range(1, 6)]

        mock_echo_objects.all.return_value = echoes

        request = self.factory.get('/api/echo-last/')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        queryset_data = [echo.id for echo in mock_echo_objects.all.return_value]


        expected_data = [1, 2, 3, 4, 5]
        self.assertEqual(queryset_data, expected_data)
