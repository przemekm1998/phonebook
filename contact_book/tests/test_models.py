from mixer.backend.django import mixer
import pytest
from contact_book.models import Person, Email, Phone
from django.contrib.auth.models import User


@pytest.fixture()
def person(db):
    yield Person(first_name='Andrzej', second_name='Hehe', owner=User())


def test_person_str(person):
    assert str(person) == 'Andrzej Hehe'


def test_email_str(person):
    email = Email(email='andrzej@gmail.com', person=person)

    assert str(email) == 'Andrzej Hehe email: andrzej@gmail.com'


def test_phone_str(person):
    phone = Phone(phone=123456789, person=person)

    assert str(phone) == 'Andrzej Hehe phone: 123456789'
