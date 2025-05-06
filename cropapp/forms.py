from django import forms
from .models import *

class Reg_Form(forms.ModelForm):

    class Meta:
        model = user
        fields = ['name', 'contact','far_address','district','state','farm_size','main_products','id_proof']

class login_form(forms.ModelForm):

    class Meta:
        model = login
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if login.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class login_verify(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class complaintform(forms.ModelForm):
    class Meta:
        model = complaint
        fields = ['comp']
        widgets = {
    'commplaint': forms.Textarea(attrs={'placeholder': 'Enter your complaint message...',
    'rows':4})
    }

class replyform(forms.ModelForm):
    class Meta:
        model = complaint
        fields = ['reply']
        widgets = {
    'commplaint': forms.Textarea(attrs={'placeholder': 'Enter your reply message...',
    'rows':4})
    }

class user_edit_form(forms.ModelForm):

    class Meta:
        model = user
        fields = ['name', 'contact','far_address','district','state','farm_size','main_products','id_proof']
        widgets = {
    'name': forms.TextInput(attrs={'class': 'form-control'}),
    'contact': forms.TextInput(attrs={'class': 'form-control'}),
    'far_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    'district': forms.TextInput(attrs={'class': 'form-control'}),
    'state': forms.TextInput(attrs={'class': 'form-control'}),
    'farm_size': forms.NumberInput(attrs={'class': 'form-control'}),
    'main_products': forms.TextInput(attrs={'class': 'form-control'}),
    'id_proof': forms.FileInput(attrs={'class': 'form-control'}),
}

class public_edit_form(forms.ModelForm):

    class Meta:
        model = public_user
        fields = ['name', 'contact']
        widgets = {
    'name': forms.TextInput(attrs={'class': 'form-control'}),
    'contact': forms.TextInput(attrs={'class': 'form-control'}),
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

class SoilDataForm(forms.Form):
    ph = forms.FloatField(label="pH Level", min_value=0, max_value=14)
    temperature = forms.FloatField(label="Temperature (°C)")
    moisture = forms.FloatField(label="Moisture (%)")
    nitrogen = forms.FloatField(label="Nitrogen (mg/kg)")
    phosphorus = forms.FloatField(label="Phosphorus (mg/kg)")
    potassium = forms.FloatField(label="Potassium (mg/kg)")

class LeafImageForm(forms.Form):
    image = forms.ImageField()