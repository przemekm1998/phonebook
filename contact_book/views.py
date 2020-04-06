from django.urls import reverse
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  DetailView, FormView)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Person, Email, Phone
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PhoneForm, PersonSearchForm, EmailSearchForm


class HomePageView(LoginRequiredMixin, FormMixin, ListView):
    """ Main home page view accessible after login """

    template_name = 'contact_book/home.html'
    model = Person
    context_object_name = 'people'
    form_class = PersonSearchForm

    def get_queryset(self):
        """ Get people list of a particular user """

        form = self.form_class(self.request.GET)
        user = User.objects.filter(username=self.request.user.username).first()
        if form.is_valid():
            if form.cleaned_data['phone']:
                return Person.objects.filter(
                    first_name__icontains=form.cleaned_data['first_name'],
                    second_name__icontains=form.cleaned_data['second_name'],
                    note__icontains=form.cleaned_data['note'],
                    owner=user).order_by('-date_added')

        return Person.objects.filter(owner=user).order_by('-date_added')


class EmailSearchView(LoginRequiredMixin, FormMixin, ListView):
    """ Search email view accessible after login """

    template_name = 'contact_book/email_search.html'
    model = Email
    context_object_name = 'emails'
    form_class = EmailSearchForm

    def get_queryset(self):
        """ Get searched email list of a particular user """

        form = self.form_class(self.request.GET)
        user = User.objects.filter(username=self.request.user.username).first()
        if form.is_valid():
            return Email.objects.filter(
                person__first_name__icontains=form.cleaned_data['first_name'],
                person__second_name__icontains=form.cleaned_data['second_name'],
                email__icontains=form.cleaned_data['email'],
                person__owner=user).order_by('-person__date_added')

        return Email.objects.filter(person_owner=user).order_by('-date_added')


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
        return Person.objects.filter(id=self.kwargs['person_id']).first()

    def post(self, request, *args, **kwargs):
        self.object = Email(person=self.person)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
        return Person.objects.filter(id=self.kwargs['person_id']).first()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        """ Check if user requesting to update person's email is it's owner """
        return True if self.request.user == self.person.owner else False


class EmailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Email

    @property
    def success_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.id})

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['person_id']).first()

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
        return Person.objects.filter(id=self.kwargs['person_id']).first()

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


class PhoneUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
                      UpdateView):
    model = Phone
    form_class = PhoneForm
    success_message = 'Phone number updated successfully'

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['person_id']).first()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        """ Check if user requesting to add phone number to person is it's owner """
        return True if self.request.user == self.person.owner else False


class PhoneDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Phone

    @property
    def success_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.id})

    @property
    def person(self):
        return Person.objects.filter(id=self.kwargs['person_id']).first()

    def test_func(self):
        """ Check if user requesting to delete an email is owner of the person which
        holds it """
        return True if self.request.user == self.person.owner else False
