import json

from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory, override_settings
from faker import Faker
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .factories import UserFactory
from .views import UserDetailView, UserSignupView

fake = Faker()


class TestUsers(APITestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.email, self.password = fake.email(), fake.password()
        self.user = UserFactory(email=self.email, password=self.password)
        self.user_credentials = dict(email=self.email, password=self.password)
        self.request_kwargs = {
            "HTTP_AUTHORIZATION": f"Bearer {self._get_access_token()}"
        }

    def _get_access_token(self):
        view = TokenObtainPairView.as_view()
        url = reverse("token_obtain_pair")
        request = self.request_factory.post(url, data=self.user_credentials)

        return json.loads(view(request).render().content.decode("utf-8"))["access"]

    def test_can_create_jwt_token(self):
        view = TokenObtainPairView.as_view()
        url = reverse("token_obtain_pair")

        request = self.request_factory.post(url, data=self.user_credentials)
        res = view(request).render()
        json_res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", json_res)
        self.assertIn("refresh", json_res)

    def test_can_refresh_jwt_token(self):
        refresh_view = TokenRefreshView.as_view()
        token_view = TokenObtainPairView.as_view()
        refresh_url = reverse("token_refresh")
        token_url = reverse("token_obtain_pair")

        data = dict(refresh="fake_refresh")
        request = self.request_factory.post(refresh_url, data=data)
        res = refresh_view(request).render()
        self.assertEqual(res.status_code, 401)  # invalid refresh token doesn't work

        token_request = self.request_factory.post(token_url, data=self.user_credentials)
        token_res = token_view(token_request).render()
        self.assertEqual(token_res.status_code, 200)  # a valid json token does work

        data = dict(refresh=json.loads(token_res.content.decode("utf-8"))["refresh"])
        request = self.request_factory.post(token_url, data=data)
        res = refresh_view(request).render()
        json_res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", json_res)

    def test_can_get_user_details(self):
        view = UserDetailView.as_view()
        url = reverse("other_user_detail", kwargs=dict(pk=self.user.id))
        request = self.request_factory.get(url, **self.request_kwargs)
        res = view(request, pk=self.user.id).render()
        json_res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)

        self.assertIn("id", json_res)
        self.assertIn("email", json_res)
        self.assertIn("geolocation", json_res)

        # test can get own users details
        url = reverse("user_detail")
        request = self.request_factory.get(url, **self.request_kwargs)
        res = view(request).render()
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(json_res["id"], self.user.id)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_user_can_sign_up(self):
        view = UserSignupView.as_view()
        url = reverse("user_signup")
        data = dict(
            email=fake.email(),
            password=fake.password()
        )
        request = self.request_factory.post(url, data=data)
        res = view(request).render()
        json_res = json.loads(res.content.decode("utf-8"))

        self.assertEqual(res.status_code, 200)
        self.assertIn("access", json_res)
        self.assertIn("refresh", json_res)
