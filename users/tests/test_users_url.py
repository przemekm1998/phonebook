from django.urls import reverse, resolve


def test_detail_register_url():
    """ Verify the returned path name """

    path = reverse('users-register')
    assert resolve(path).view_name == 'users-register'


def test_detail_login_url():
    """ Verify the returned path name """

    path = reverse('users-login')
    assert resolve(path).view_name == 'users-login'
