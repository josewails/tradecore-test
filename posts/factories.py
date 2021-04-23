import factory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'posts.Post'

    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
    user = factory.SubFactory("users.User")
