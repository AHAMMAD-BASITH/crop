from django.db import models

# Create your models here.
class login(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    user_type = models.CharField(max_length=20)

class user(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_id=models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True)

class public_user(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_id=models.OneToOneField(login,on_delete=models.CASCADE,null=True,blank=True,related_name='us')


class products(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    price = models.CharField(max_length=5)
    login_id=models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True)

class cart(models.Model):
    product_id = models.ForeignKey(products,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True,related_name='users')
    payment_status = models.IntegerField(default=0)
    cancelation_status = models.IntegerField(default=0)
    current_date = models.DateTimeField(auto_now_add=True)

class payment(models.Model):
    onwer_name = models.CharField(max_length=25)
    card_no = models.CharField(max_length=15)
    cvv = models.CharField(max_length=5)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    amount = models.IntegerField(default=0)
    cart_id = models.ForeignKey(cart,on_delete=models.CASCADE,null=True,blank=True)
    login_id = models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True)
    current_date = models.DateTimeField(auto_now_add=True)


class alert(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)