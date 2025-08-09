from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import MyCircle
from django.contrib.auth import get_user_model
from .models import Expense

class SignupForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','phone','address','password1','password2']

class LoginForm(forms.Form):
    email=forms.EmailField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)

User=get_user_model()
class MyCircleForm(forms.ModelForm):
    class Meta:
        model = MyCircle
        fields = ['name', 'description']

User=get_user_model()
class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        fields=['description','amount','date','category']

        widgets={'date':forms.DateInput(attrs={'type':'date'})}


