import datetime
from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute
from random import randint


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    first_name = 'John'
    last_name = 'Doe'
    username = lazy_attribute(
        lambda o: slugify(o.first_name + '.' + o.last_name)
    )
    email = lazy_attribute(lambda o: o.username + "@example.com")

    @lazy_attribute
    def date_joined(self):
        return datetime.datetime.now() - datetime.timedelta(
            days=randint(5, 50)
        )
    last_login = lazy_attribute(
        lambda o: o.date_joined + datetime.timedelta(days=4)
    )


class BrokenFactory(DjangoModelFactory):

    class Meta:
        model = 'nonExistingModel'


class BrokenFactoryWithoutMetaClass(DjangoModelFactory):
    pass


class BrokenFactoryClassDoesNotInheritFromDjangoModelFactory():
    class Meta:
        model = 'auth.User'
