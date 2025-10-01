from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Expense, Income, RecurringExpense

# Custom form for user creation, extending Django's built-in UserCreationForm.
# This form is used to allow users to sign up with an additional 'role' field.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Specifies the custom User model to be used for this form.
        model = User
        # Includes all default fields from UserCreationForm, plus the custom 'role' field.
        fields = UserCreationForm.Meta.fields + ('role',)

# Form for Expense model.
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        # Fields to be included in the form, now including 'currency'.
        fields = ['description', 'amount', 'currency', 'date', 'category']
        # Widgets to customize the appearance and behavior of form fields.
        widgets = {
            # Uses an HTML5 date input for a native calendar picker.
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for Income model.
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        # Fields to be included in the form, now including 'currency'.
        fields = ['description', 'amount', 'currency', 'date']
        # Widgets to customize the appearance and behavior of form fields.
        widgets = {
            # Uses an HTML5 date input for a native calendar picker.
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for RecurringExpense model.
class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        # Fields to be included in the form, now including 'currency'.
        fields = ['description', 'amount', 'currency', 'frequency', 'start_date', 'end_date']
        # Widgets to customize the appearance and behavior of form fields.
        widgets = {
            # Uses HTML5 date inputs for native calendar pickers.
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }