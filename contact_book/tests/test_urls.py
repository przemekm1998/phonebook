from django.urls import reverse, resolve


class TestUrls:

    def test_detail_url(self):
        """ Verify the returned path name """

        path = reverse('home')
        assert resolve(path).view_name == 'home'
