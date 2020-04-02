from django.urls import path

from .views import HomePageView, PersonCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add/person/', PersonCreateView.as_view(), name='create-person')
]
