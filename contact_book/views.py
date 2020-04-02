from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Person, Email


class HomePageView(LoginRequiredMixin, ListView):
    """ Main home page view accessible after login """

    template_name = 'contact_book/home.html'
    model = Person
    context_object_name = 'people'

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username).first()
        return Person.objects.filter(owner=user).order_by('-date_added')


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'second_name', 'note']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EmailCreateView(LoginRequiredMixin, CreateView):
    model = Email
    fields = ['email', 'person']

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username).first()
        return Person.objects.filter(owner=user).order_by('-second_name')
