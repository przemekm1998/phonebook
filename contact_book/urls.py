from django.urls import path

from .views import (HomePageView, PersonCreateView, PersonUpdateView,
                    PersonDeleteView, PersonDetailView, EmailCreateView,
                    EmailUpdateView, EmailDeleteView, PhoneCreateView,
                    PhoneUpdateView, PhoneDeleteView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('person/add/', PersonCreateView.as_view(), name='create-person'),
    path('person/update/<int:pk>/', PersonUpdateView.as_view(), name='update-person'),
    path('person/delete/<int:pk>/', PersonDeleteView.as_view(), name='delete-person'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='detail-person'),
    path('email/create/<int:person_id>/', EmailCreateView.as_view(),
         name='email-create'),
    path('email/update/<int:person_id>/<int:pk>/', EmailUpdateView.as_view(),
         name='email-update'),
    path('email/delete/<int:person_id>/<int:pk>/', EmailDeleteView.as_view(),
         name='email-delete'),
    path('phone/create/<int:person_id>/', PhoneCreateView.as_view(),
         name='phone-create'),
    path('phone/update/<int:person_id>/<int:pk>/', PhoneUpdateView.as_view(),
         name='phone-update'),
    path('phone/delete/<int:person_id>/<int:pk>/', PhoneDeleteView.as_view(),
         name='phone-delete')
]
