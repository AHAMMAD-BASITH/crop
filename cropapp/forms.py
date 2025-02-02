from django import forms
from .models import login,user,public_user,products,payment

class Reg_Form(forms.ModelForm):

    class Meta:
        model = user
        fields = ['name', 'contact']

class login_form(forms.ModelForm):

    class Meta:
        model = login
        fields = ['email', 'password']

class login_verify(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class user_edit_form(forms.ModelForm):

    class Meta:
        model = user
        fields = ['name', 'contact']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'contact':forms.TextInput(attrs={'class':'form-control'})
        }
   

class login_edit_form(forms.ModelForm):

    class Meta:
        model = login
        fields = ['email']
        widgets = {
            'email':forms.TextInput(attrs={'class':'form-control'})
        }

        
class public_Form(forms.ModelForm):

    class Meta:
        model = public_user
        fields = ['name', 'contact']


class products_form(forms.ModelForm):
    class Meta:
        model=products
        fields=['category','name','image','price']


class payment_form(forms.ModelForm):
    exp_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        input_formats=['%d-%m-%Y']  # Accept DD-MM-YYYY format
    )
    class Meta:
        model=payment
        fields=['onwer_name','card_no','cvv','exp_date']