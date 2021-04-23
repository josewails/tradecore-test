import random
import json

from django.urls import reverse

from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework_simplejwt.views import TokenObtainPairView
from faker import Faker

from users.factories import UserFactory
from .factories import PostFactory
from .views import PostViewSet

fake = Faker()


class TestPosts(APITestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.email, self.password = fake.email(), fake.password()
        self.user_one = UserFactory(email=self.email, password=self.password)
        self.users = [UserFactory(password=fake.password()) for _ in range(5)]
        self.request_kwargs = {
            "HTTP_AUTHORIZATION": f"Bearer {self._get_access_token()}"
        }
        self.posts = [PostFactory(user=random.choice(self.users)) for _ in range(5)]

    def _get_access_token(self):
        view = TokenObtainPairView.as_view()
        url = reverse("token_obtain_pair")
        request = self.request_factory.post(url, data=dict(email=self.email, password=self.password))
        res = view(request).render()
        return json.loads(res.content.decode("utf-8"))["access"]

    def test_can_create_post(self):
        data = dict(
            title=fake.sentence(),
            body=fake.paragraph(),
            user=self.user_one.id
        )
        request = self.request_factory.post("/posts", **self.request_kwargs, data=data)
        view = PostViewSet.as_view({"post": "create"})
        res = view(request).render()
        json_res = json.loads(res.content.decode("utf-8"))

        self.assertEqual(res.status_code, 201)
        self.assertIn("title", json_res)
        self.assertEqual(json_res["title"], data["title"])

    def test_can_retrieve_post(self):
        post = self.posts[random.randint(0, 4)]
        request = self.request_factory.get(f"/posts/{post.id}", **self.request_kwargs)
        view = PostViewSet.as_view({"get": "retrieve"})
        res = view(request, pk=post.id).render()
        json_res = json.loads(res.content.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertIn("title", json_res)

    def test_can_list_posts(self):
        request = self.request_factory.get("posts/", **self.request_kwargs)
        view = PostViewSet.as_view({"get": "list"})
        res = view(request).render()
        json_res = json.loads(res.content.decode("utf-8"))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_res), 5)

    def test_can_update_post(self):
        post = self.posts[random.randint(0, 4)]
        initial_title = post.title
        data = dict(
            title=fake.sentence(),
            body=fake.paragraph(),
            user=self.user_one.id
        )
        request = self.request_factory.post(f"/posts/{post.id}", data=data, **self.request_kwargs)
        view = PostViewSet.as_view({"post": "update"})
        res = view(request, pk=post.id).render()

        self.assertEqual(res.status_code, 200)
        post.refresh_from_db()
        self.assertNotEqual(post.title, initial_title)
