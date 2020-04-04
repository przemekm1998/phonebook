from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    """ Person model """

    first_name = models.CharField(max_length=20, null=False)
    second_name = models.CharField(max_length=30, null=False)
    date_added = models.DateTimeField(default=timezone.now)
    note = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

    @staticmethod
    def get_absolute_url():
        return reverse('home')


class Email(models.Model):
    """ Email model """

    email = models.EmailField(null=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.person)} email: {self.email}'

    def get_absolute_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.pk})


class Phone(models.Model):
    """ Phone model """

    phone = models.IntegerField(null=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def validate_unique(self, exclude=None):
        qs = Phone.objects.filter(phone=self.phone).all()
        if qs.filter(person=self.person).exists():
            raise ValidationError("Phone number for this person already exists")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Phone, self).save(*args, **kwargs)

    def __str__(self):
        return f'{str(self.person)} phone: {self.phone}'

    def get_absolute_url(self):
        return reverse('detail-person', kwargs={'pk': self.person.pk})
