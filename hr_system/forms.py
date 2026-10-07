from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date

# Import your models from models.py
from .models import AttendanceRequest, EmployeeProfile

# ---------------------------------------------------------
# 1. THE LEAVE REQUEST FORM
# ---------------------------------------------------------
class AttendanceRequestForm(forms.ModelForm):
    class Meta:
        model = AttendanceRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Block past dates
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today_string = date.today().strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs['min'] = today_string
        self.fields['end_date'].widget.attrs['min'] = today_string

# ---------------------------------------------------------
# 2. THE EMPLOYEE REGISTRATION FORM
# ---------------------------------------------------------
class EmployeeRegistrationForm(UserCreationForm):
    # Custom fields for the HR UI
    full_name = forms.CharField(max_length=100, required=True)
    employee_id = forms.CharField(max_length=20, required=True)
    
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('SALES', 'Sales'),
        ('OPS', 'Operations'),
        ('FIN', 'Finance'),
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    # Intercept the save process to create BOTH the User and the Profile at once
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Automatically create the HR profile using the form data
            EmployeeProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                employee_id=self.cleaned_data['employee_id'],
                department=self.cleaned_data['department']
            )
        return user