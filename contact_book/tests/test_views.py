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


@pytest.fixture(scope='function')
def specific_user(db):
    yield mixer.blend(User, values={'username': 'przemek', 'id': 1})


@pytest.fixture(scope='function')
def specific_person(db, specific_user):
    yield mixer.blend(Person, values={'id': 1, 'owner': specific_user})


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


@pytest.mark.parametrize('user, response_code',
                         [
                             (User(), 200),
                             (AnonymousUser(), 302)
                         ])
def test_person_add_authentication(user, response_code, factory, db):
    """ Verify if person adding is accessible if user is authenticated """

    path = reverse('create-person')
    request = factory.get(path)
    request.user = user

    response = HomePageView.as_view()(request)

    assert response.status_code == response_code


def test_person_edit_authentication_correct_user(factory, specific_user,
                                                 specific_person, db):
    """
    Verify if person editing is accessible if user is authenticated and created the
    person.
    """

    path = reverse('update-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = specific_user

    response = HomePageView.as_view()(request)

    assert response.status_code == 200


def test_person_edit_authentication_anonymous_user(factory, specific_person, db):
    """
    Verify if person editing is accessible if user is unauthenticated
    """

    path = reverse('update-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = HomePageView.as_view()(request)

    assert response.status_code == 302


def test_person_delete_authentication_correct_user(factory, specific_user,
                                                   specific_person, db):
    """
    Verify if person deleting is accessible if user is authenticated and created the
    person.
    """

    path = reverse('delete-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = specific_user

    response = HomePageView.as_view()(request)

    assert response.status_code == 200


def test_person_delete_authentication_anonymous_user(factory, specific_person, db):
    """
    Verify if person deleting is accessible if user is unauthenticated
    """

    path = reverse('delete-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = HomePageView.as_view()(request)

    assert response.status_code == 302


def test_person_detail_authentication_correct_user(factory, specific_user,
                                                   specific_person, db):
    """
    Verify if person detail is accessible if user is authenticated and created the
    person.
    """

    path = reverse('detail-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = specific_user

    response = HomePageView.as_view()(request)

    assert response.status_code == 200


def test_person_detail_authentication_anonymous_user(factory, specific_person, db):
    """
    Verify if person detail is accessible if user is unauthenticated
    """

    path = reverse('detail-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = HomePageView.as_view()(request)

    assert response.status_code == 302

# def test_person_edit_authentication_incorrect_user(factory, db, specific_user):
#     """
#     Verify if person editing is not accessible if user is authenticated and
#     didn't create the person.
#     """
#
#     Person(first_name='cos', second_name='tam', owner=specific_user).save()
#     print(Person.objects.filter(owner=specific_user).first().id)
#
#     path = reverse('update-person', kwargs={'pk': 1})
#     request = factory.get(path)
#     request.user =
#
#     response = HomePageView.as_view()(request, id=1)
#     print(str(response))

# assert response.status_code == 403
