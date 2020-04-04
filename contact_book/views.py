from django.urls import reverse
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  DetailView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Person, Email, Phone
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PhoneForm


class HomePageView(LoginRequiredMixin, ListView):
    """ Main home page view accessible after login """

    template_name = 'contact_book/home.html'
    model = Person
    context_object_name = 'people'

    def get_queryset(self):
        """ Get people list of a particular user """
        user = User.objects.filter(username=self.request.user.username).first()
        return Person.objects.filter(owner=user).order_by('-date_added')


class PersonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Person
    fields = ['first_name', 'second_name', 'note']
    success_message = 'Person created successfully!'

    def form_valid(self, form):
        """ Setting the owner of a person as a currenctly logged user """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PersonUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin,
                       UpdateView):
    model = Person
    fields = ['first_name', 'second_name', 'note']
    success_message = 'Person updated successfully'

    def test_func(self):
        """ Check if user requesting to update a person is it's owner """
        person = self.get_object()
        return True if self.request.user == person.owner else False

    def form_valid(self, form):
        """ Setting the owner of a person as a currenctly logged user """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PersonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person
    success_url = '/'

    def test_func(self):
        """ Check if user requesting to delete a person is it's owner """
        person = self.get_object()
        return True if self.request.user == person.owner else False


class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person

    def test_func(self):
        """ Check if user requesting to see the details of a person is it's owner """
        person = self.get_object()
        return True if self.request.user == person.owner else False


class EmailCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
                      CreateView):
    model = Email
    fields = ['email']
    success_message = 'Email created successfully'

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['pk']).first()

    def form_valid(self, form):
        """
        Setting the email's owner automatically to the person being currently
        listed
         """
        form.instance.person = self.person
        return super().form_valid(form)

    def test_func(self):
        """ Check if user requesting to add email to a person is it's owner """
        return True if self.request.user == self.person.owner else False


class EmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin,
                      UpdateView):
    model = Email
    fields = ['email']
    success_message = 'Email updated successfully'

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['pk']).first()

    def form_valid(self, form):
        """
        Setting the email's owner automatically to the person being currently
        listed
         """
        form.instance.person = self.person
        return super().form_valid(form)

    def test_func(self):
        """ Check if user requesting to update person's email is it's owner """
        return True if self.request.user == self.person.owner else False


class EmailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person

    @property
    def success_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.id})

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['pk']).first()

    def test_func(self):
        """ Check if user requesting to delete an email is owner of the person which
        holds it """
        return True if self.request.user == self.person.owner else False


class PhoneCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
                      CreateView):
    model = Phone
    form_class = PhoneForm
    success_message = 'Phone number created successfully'

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['pk']).first()

    def post(self, request, *args, **kwargs):
        self.object = Phone(person=self.person)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        """ Check if user requesting to add phone number to person is it's owner """
        return True if self.request.user == self.person.owner else False
