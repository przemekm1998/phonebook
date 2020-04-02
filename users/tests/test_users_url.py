from django.urls import reverse, resolve


def test_detail_register_url():
    """ Verify the returned path name """

    path = reverse('users-register')
    assert resolve(path).view_name == 'users-register'


def test_detail_login_url():
    """ Verify the returned path name """

    path = reverse('users-login')
    assert resolve(path).view_name == 'users-login'


def test_detail_password_reset_url():
    """ Verify the returned path name """

    path = reverse('password_reset')
    assert resolve(path).view_name == 'password_reset'


def test_detail_password_reset_done_url():
    """ Verify the returned path name """

    path = reverse('password_reset_done')
    assert resolve(path).view_name == 'password_reset_done'


def test_detail_password_reset_complete_url():
    """ Verify the returned path name """

    path = reverse('password_reset_complete')
    assert resolve(path).view_name == 'password_reset_complete'
