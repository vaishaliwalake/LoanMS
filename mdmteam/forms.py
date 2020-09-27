from django import forms

class TestForm(forms.Form):

    # HTMl INPUT Box
    LoanID = forms.IntegerField()
    CreditScoreMin = forms.IntegerField()
    CreditScoreMax = forms.IntegerField()
    LoanAmountMin = forms.IntegerField()
    LoanAmountMax = forms.IntegerField()
    IntrestRatePct = forms.IntegerField()
    DurationMonths = forms.IntegerField()
    eff_from_date = forms.IntegerField() # forms.DateField( widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    eff_to_date = forms.IntegerField() # forms.DateField( widget=forms.widgets.DateInput(format="%m/%d/%Y"))

class DeleteForm(forms.Form):
    LoanID = forms.IntegerField ()

class UpdateForm(forms.Form):
    LoanID = forms.IntegerField (required=False)
    CreditScoreMin = forms.IntegerField (required=False)
    CreditScoreMax = forms.IntegerField (required=False)
    LoanAmountMin = forms.IntegerField (required=False)
    LoanAmountMax = forms.IntegerField (required=False)
    IntrestRatePct = forms.IntegerField (required=False)
    DurationMonths = forms.IntegerField (required=False)
    eff_from_date = forms.DateField ()  # forms.DateField( widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    eff_to_date = forms.DateField ()


