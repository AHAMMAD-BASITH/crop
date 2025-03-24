from django import forms
from .models import *

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
    class Meta:
        model=payment
        fields=['onwer_name','card_no','cvv','exp_month','exp_year']

class farmer_payment_form(forms.ModelForm):
    class Meta:
        model=farmer_payment
        fields=['onwer_name','card_no','cvv','exp_month','exp_year']

class AlertForm(forms.ModelForm):
    class Meta:
        model = alert
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter your alert message...', 'rows': 4}),
        }

class gov_products_form(forms.ModelForm):
    class Meta:
        model=gov_products
        fields=['category','name','image','price','subsidy_price']

class NotificatioForm(forms.ModelForm):
    class Meta:
        model = notification
        fields = ['message'] 
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter the notification...', 'rows': 4}),
        }

class address_form(forms.ModelForm):
    class Meta:
        model=address
        fields=['name','contact','house_name','area','landmark','pincode','city','state']

class deliver_Form(forms.ModelForm):

    class Meta:
        model = delivery_boy
        fields = ['name', 'contact']