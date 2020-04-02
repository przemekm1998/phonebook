from django.urls import reverse, resolve


def test_detail_url():
    """ Verify the returned path name """

    path = reverse('home')
    assert resolve(path).view_name == 'home'
