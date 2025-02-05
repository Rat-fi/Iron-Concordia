from django import forms

class BudgetForm(forms.Form):
    budget = forms.DecimalField(max_digits=6, decimal_places=2, label='Enter your budget...')
