from abc import ABC, abstractmethod
from . models import User
import factory
from faker import Faker
from asgiref.sync import sync_to_async


class DataSource(ABC):
    @abstractmethod
    def query(self, **kwargs):
        ...

    @property
    @abstractmethod
    def name(self):
        ...


class FilterDBData(DataSource):

    def __init__(self, name):
        self._name = name

    def query(self, **kwargs):

        filters = dict()
        if kwargs['first_name']:
            filters['first_name'] = kwargs['first_name']
        if kwargs['last_name']:
            filters['last_name'] = kwargs['last_name']
        if kwargs['email']:
            filters['email'] = kwargs['email']

        users = User.objects.using(self.name).filter(**filters)

        result = []
        for user in users:
            user_object = dict()
            user_object["first_name"] = user.first_name
            user_object["last_name"] = user.last_name
            user_object["email"] = user.email
            user_object["db"] = self.name
            result.append(user_object)

        return result

    @property
    def name(self):
        return self._name


fake = Faker()


def generate_username(*args):
    return fake.profile(fields=['username'])['username']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.LazyAttribute(generate_username)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


def create_dummy_data_for_db(db, count):
    users = UserFactory.create_batch(count)
    User.objects.using(db).bulk_create(users)


@sync_to_async
def add_db_match_to_users(users, default_db_users):
    for user in default_db_users:
        users.append(user)
    return users
