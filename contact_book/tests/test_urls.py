from django.urls import reverse, resolve


def test_detail_home_url():
    """ Verify the returned path name """

    path = reverse('home')
    assert resolve(path).view_name == 'home'


def test_detail_person_add_url():
    """ Verify the returned path name """

    path = reverse('create-person')
    assert resolve(path).view_name == 'create-person'


def test_detail_person_update_url():
    """ Verify the returned path name """

    path = reverse('update-person', kwargs={'pk': 1})
    assert resolve(path).view_name == 'update-person'


def test_detail_person_delete_url():
    """ Verify the returned path name """

    path = reverse('delete-person', kwargs={'pk': 1})
    assert resolve(path).view_name == 'delete-person'


def test_detail_person_detail_url():
    """ Verify the returned path name """

    path = reverse('detail-person', kwargs={'pk': 1})
    assert resolve(path).view_name == 'detail-person'
