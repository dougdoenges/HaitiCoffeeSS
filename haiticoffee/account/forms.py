from django import forms

class NewAddressForm(forms.Form):
    addressLine1 = forms.CharField(label='Address Line 1', max_length=250, required=True)
    addressLine2 = forms.CharField(label='Address Line 2', max_length=250, required=False)
    city = forms.CharField(label='City', max_length=250, required=True)
    state = forms.CharField(label='State', max_length=30, required=True)
    postalCode = forms.CharField(label='Postal Code', max_length=10, required=True)
    country = forms.CharField(label='Country', max_length=250, required=True)



class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=forms.PasswordInput)
    passwordconf = forms.CharField(label='Passwordconf', max_length=30, required=True, widget=forms.PasswordInput)
    email = forms.CharField(label='email', max_length=30, required=True)
    first_name = forms.CharField(label='first_name', max_length=30, required=True)
    last_name = forms.CharField(label='last_name', max_length=30, required=True)

class SigninForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=forms.PasswordInput)