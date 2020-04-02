import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from contact_book.views import HomePageView
from contact_book.models import Person


@pytest.fixture(scope='module')
def factory():
    yield RequestFactory()


@pytest.mark.parametrize('user, response_code',
                         [
                             (User(), 200),
                             (AnonymousUser(), 302)
                         ])
def test_home_view_authentication(user, response_code, factory, db):
    """ Verify if home page is accessible if user is authenticated """

    path = reverse('home')
    request = factory.get(path)
    request.user = user

    response = HomePageView.as_view()(request)

    assert response.status_code == response_code
