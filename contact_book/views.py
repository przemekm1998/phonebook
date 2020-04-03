from django.urls import reverse
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Person, Email
from django.contrib.messages.views import SuccessMessageMixin


class HomePageView(LoginRequiredMixin, ListView):
    """ Main home page view accessible after login """

    template_name = 'contact_book/home.html'
    model = Person
    context_object_name = 'people'

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username).first()
        return Person.objects.filter(owner=user).order_by('-date_added')


class PersonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Person
    fields = ['first_name', 'second_name', 'note']
    success_message = 'Person created successfully!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PersonUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin,
                       UpdateView):
    model = Person
    fields = ['first_name', 'second_name', 'note']
    success_message = 'Person updated successfully'

    def test_func(self):
        person = self.get_object()
        return True if self.request.user == person.owner else False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PersonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person
    success_url = '/'

    def test_func(self):
        person = self.get_object()
        return True if self.request.user == person.owner else False


class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person

    def test_func(self):
        person = self.get_object()
        return True if self.request.user == person.owner else False


class EmailCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
                      CreateView):
    model = Email
    fields = ['email']
    success_message = 'Email created successfully'

    def form_valid(self, form):
        person = Person.objects.filter(id=self.kwargs['pk']).first()
        form.instance.person = person
        return super().form_valid(form)

    def test_func(self):
        person = Person.objects.filter(id=self.kwargs['pk']).first()
        return True if self.request.user == person.owner else False


class EmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin,
                      UpdateView):
    model = Email
    fields = ['email']
    success_message = 'Email updated successfully'

    def form_valid(self, form):
        person = Person.objects.filter(id=self.kwargs['person_id']).first()
        form.instance.person = person
        return super().form_valid(form)

    def test_func(self):
        person = Person.objects.filter(id=self.kwargs['person_id']).first()
        return True if self.request.user == person.owner else False


class EmailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person

    @property
    def success_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.id})

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['pk']).first()

    def test_func(self):
        return True if self.request.user == self.person.owner else False


class EmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin,
                      UpdateView):
    model = Email
    fields = ['email']
    success_message = 'Email updated successfully'

    def form_valid(self, form):
        person = Person.objects.filter(id=self.kwargs['person_id']).first()
        form.instance.person = person
        return super().form_valid(form)

    def test_func(self):
        person = Person.objects.filter(id=self.kwargs['person_id']).first()
        return True if self.request.user == person.owner else False


class EmailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Email

    @property
    def success_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.id})

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['person_id']).first()

    def test_func(self):
        return True if self.request.user == self.person.owner else False
