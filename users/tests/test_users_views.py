import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from users.views import RegisterView


@pytest.fixture(scope='module')
def factory():
    yield RequestFactory()


@pytest.mark.parametrize('user, response_code',
                         [
                             (User(), 200),
                             (AnonymousUser(), 200)
                         ])
def test_register_view_authentication(user, response_code, factory, db):
    """ Verify if register page is accessible """

    path = reverse('users-register')
    request = factory.get(path)
    request.user = user

    response = RegisterView.as_view()(request)

    assert response.status_code == response_code


@pytest.mark.parametrize('user, response_code',
                         [
                             (User(), 200),
                             (AnonymousUser(), 200)
                         ])
def test_login_view_authentication(user, response_code, factory, db):
    """ Verify if login page is accessible"""

    path = reverse('users-login')
    request = factory.get(path)
    request.user = user

    response = RegisterView.as_view()(request)

    assert response.status_code == response_code
