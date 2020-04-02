from django.contrib import admin
from .models import Person, Email, Phone

admin.site.register(Person)
admin.site.register(Email)
admin.site.register(Phone)
