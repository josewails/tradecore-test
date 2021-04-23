import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    email = factory.Faker("email")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        user = manager.create_user(*args, **kwargs)
        user.set_password(kwargs.pop("password"))
        user.save()

        return user
