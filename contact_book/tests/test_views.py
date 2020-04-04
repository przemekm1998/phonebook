import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from contact_book.views import (HomePageView, EmailCreateView, PersonCreateView,
                                PersonUpdateView, PersonDeleteView, PersonDetailView,
                                EmailCreateView, EmailUpdateView, EmailDeleteView)
from contact_book.models import Person, Email
from django.core.exceptions import PermissionDenied


@pytest.fixture(scope='module')
def factory():
    yield RequestFactory()


@pytest.fixture(scope='function')
def user(db):
    yield mixer.blend(User)


@pytest.fixture(scope='function')
def person(db):
    yield mixer.blend(Person)


@pytest.fixture(scope='function')
def email(db):
    yield mixer.blend(Email)


@pytest.mark.parametrize('user, response_code',
                         [
                             (User(), 200),
                             (AnonymousUser(), 302)
                         ])
def test_home_view_authentication(user, response_code, factory, db):
    """ Verify if home page is accessible based on authentication """

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

    response = PersonCreateView.as_view()(request)

    assert response.status_code == response_code


def test_person_edit_correct_user(factory, user,
                                  person, db):
    """
    Verify if person editing is accessible if user is authenticated and created the
    person.
    """

    path = reverse('update-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = person.owner

    response = PersonUpdateView.as_view()(request, pk=1)

    assert response.status_code == 200


def test_person_edit_incorrect_user(factory, user,
                                    person, db):
    """
    Verify if person editing is not accessible if user is authenticated and didn't
    create the person.
    """

    path = reverse('update-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = PersonUpdateView.as_view()(request, pk=1)


def test_person_edit_anonymous_user(factory, db):
    """
    Verify if person editing is not accessible if user is unauthenticated
    """

    path = reverse('update-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = PersonUpdateView.as_view()(request)

    assert response.status_code == 302


def test_person_delete_correct_user(factory, user,
                                    person, db):
    """
    Verify if person deleting is accessible if user is authenticated and created the
    person.
    """

    path = reverse('delete-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = person.owner

    response = PersonDeleteView.as_view()(request, pk=1)

    assert response.status_code == 200


def test_person_delete_incorrect_user(factory, user,
                                      person, db):
    """
    Verify if person deleting is not accessible if user is authenticated and didn't
    create the person.
    """

    path = reverse('delete-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = PersonDeleteView.as_view()(request, pk=1)


def test_person_delete_anonymous_user(factory, person, db):
    """
    Verify if person deleting is not accessible if user is unauthenticated
    """

    path = reverse('delete-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = PersonDeleteView.as_view()(request, pk=1)

    assert response.status_code == 302


def test_person_detail_correct_user(factory, user,
                                    person, db):
    """
    Verify if person detail is accessible if user is authenticated and created the
    person.
    """

    path = reverse('detail-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = person.owner

    response = PersonDetailView.as_view()(request, pk=1)

    assert response.status_code == 200


def test_person_detail_incorrect_user(factory, user,
                                      person, db):
    """
    Verify if person detail is not accessible if user is authenticated and didn't
    create the person.
    """

    path = reverse('detail-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = PersonDetailView.as_view()(request, pk=1)


def test_person_detail_anonymous_user(factory, person, db):
    """
    Verify if person detail is not accessible if user is unauthenticated
    """

    path = reverse('detail-person', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = PersonDetailView.as_view()(request, pk=1)

    assert response.status_code == 302


def test_email_create_correct_user(factory, user,
                                   person, db):
    """
    Verify if email creation is accessible if user is authenticated and created the
    person.
    """

    path = reverse('email-create', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = person.owner

    response = EmailCreateView.as_view()(request, pk=1)

    assert response.status_code == 200


def test_email_create_incorrect_user(factory, user,
                                     person, db):
    """
    Verify if create email is not accessible if user is authenticated and didn't
    create the person.
    """

    path = reverse('email-create', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = EmailCreateView.as_view()(request, pk=1)


def test_email_create_anonymous_user(factory, person, db):
    """
    Verify if create email is not accessible if user is unauthenticated
    """

    path = reverse('email-create', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = EmailCreateView.as_view()(request, pk=1)

    assert response.status_code == 302


def test_email_edit_correct_user(factory, user,
                                 person, db, email):
    """
    Verify if email editing is accessible if user is authenticated and created the
    person.
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = person.owner

    response = EmailUpdateView.as_view()(request, pk=1, person_id=1)

    assert response.status_code == 200


def test_email_edit_incorrect_user(factory, user,
                                   person, db, email):
    """
    Verify if email edit is not accessible if user is authenticated and
    didn't create the person.
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = EmailUpdateView.as_view()(request, pk=1, person_id=1)


def test_email_edit_anonymous_user(factory, person, db, email):
    """
    Verify if email update is not accessible if user is unauthenticated
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = EmailUpdateView.as_view()(request, pk=1, person_id=1)

    assert response.status_code == 302


def test_email_delete_correct_user(factory, user,
                                   person, db, email):
    """
    Verify if email deleting is accessible if user is authenticated and created the
    person.
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = person.owner

    response = EmailDeleteView.as_view()(request, pk=1, person_id=1)

    assert response.status_code == 200


def test_email_delete_incorrect_user(factory, user,
                                     person, db, email):
    """
    Verify if email deleting is not accessible if user is authenticated and
    didn't create the person.
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = user

    with pytest.raises(PermissionDenied):
        response = EmailDeleteView.as_view()(request, pk=1, person_id=1)


def test_email_delete_anonymous_user(factory, person, db, email):
    """
    Verify if email deleting is not accessible if user is unauthenticated
    """

    path = reverse('email-update', kwargs={'pk': 1, 'person_id': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = EmailDeleteView.as_view()(request, pk=1, person_id=1)

    assert response.status_code == 302
