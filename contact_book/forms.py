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


class PersonSearchForm(forms.Form):
    first_name = forms.CharField(required=False, label='Search first name',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'John'}))

    second_name = forms.CharField(required=False, label='Search second name',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Doe'}))

    note = forms.CharField(required=False, label='Search note',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Some note'}))

    phone = forms.IntegerField(required=False, label='Search phone number',
                               widget=forms.TextInput(
                                   attrs={'placeholder': '111222333'}))


class EmailSearchForm(forms.Form):
    first_name = forms.CharField(required=False, label='Search first name',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'John'}))

    second_name = forms.CharField(required=False, label='Search second name',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Doe'}))

    email = forms.CharField(required=False, label='Search email',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'john.doe@example.com'}))
