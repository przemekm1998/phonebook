from django.urls import path

from .views import (HomePageView, PersonCreateView, PersonUpdateView,
                    PersonDeleteView, PersonDetailView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('person/add/', PersonCreateView.as_view(), name='create-person'),
    path('person/update/<int:pk>/', PersonUpdateView.as_view(), name='update-person'),
    path('person/delete/<int:pk>/', PersonDeleteView.as_view(), name='delete-person'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='detail-person')
]
