from django import forms
from django import forms

from selfserv.models import Customers,Login


class CustomerForm(forms.ModelForm):
    cust_id = forms.IntegerField ()
    first_name = forms.CharField ()
    last_name = forms.CharField ()
    email = forms.CharField ()

    class Meta:
         model = Customers
         fields = ['first_name', 'last_name', 'email','CreditScore','DurationInMonths','RequestedLoanAmount','cust_id']


class LoginForm (forms.ModelForm):
    class Meta:
        model = Login
        fields = ['first_name', 'last_name', 'email', 'password', 'username']


from django import forms



class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Login
        fields = ('first_name', 'last_name', 'email', 'password', 'username' )

