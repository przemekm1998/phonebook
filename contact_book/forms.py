from django import forms
from .models import Phone, Person


class PhoneForm(forms.ModelForm):
    """ Phone number adding custom form """

    phone_num_length = 9  # Const length of phone number

    class Meta:
        model = Phone
        fields = ['phone']

    def clean_phone(self):
        """ Verifying input phone number """
        phone = self.cleaned_data['phone']

        if len(str(phone)) != PhoneForm.phone_num_length:
            raise forms.ValidationError(
                f'Number should contain {self.phone_num_length} digits: {phone}',
                code='invalid')

        return phone
