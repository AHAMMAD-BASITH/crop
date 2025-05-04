from django.db import models

# Create your models here.
class login(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    user_type = models.CharField(max_length=20)
    verification_status=models.IntegerField(default=0)
    gov_status=models.IntegerField(default=0)

class user(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    login_id=models.OneToOneField(login,on_delete=models.CASCADE,null=True,blank=True,related_name='far')
    far_address=models.CharField(max_length=200)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    farm_size=models.IntegerField(default=0)
    main_products=models.CharField(max_length=200)
    id_proof = models.FileField(upload_to='id_proofs/')


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

class complaint(models.Model):
    comp=models.CharField(max_length=50)
    reply=models.CharField(max_length=500,null=True)
    currentdate=models.DateTimeField(auto_now_add=True)
    userid=models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True)
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,null=True,blank=True)

class cart(models.Model):
    product_id = models.ForeignKey(products,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True,related_name='users')
    payment_status = models.IntegerField(default=0)
    cancelation_status = models.IntegerField(default=0)
    delivery_status = models.IntegerField(default=0)
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

class gov_products(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    price = models.CharField(max_length=10)
    subsidy_price = models.CharField(max_length=10)
    current_date = models.DateTimeField(auto_now=True)

class farmer_cart(models.Model):
    product_id = models.ForeignKey(gov_products,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True,related_name='farmer')
    payment_status = models.IntegerField(default=0)
    cancelation_status = models.IntegerField(default=0)
    current_date = models.DateTimeField(auto_now_add=True)

class farmer_payment(models.Model):
    onwer_name = models.CharField(max_length=25)
    card_no = models.CharField(max_length=15)
    cvv = models.CharField(max_length=5)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    amount = models.IntegerField(default=0)
    cart_id = models.ForeignKey(farmer_cart,on_delete=models.CASCADE,null=True,blank=True)
    login_id = models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True)
    current_date = models.DateTimeField(auto_now_add=True)

class notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

class address(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    house_name=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    login_id=models.ForeignKey(login,on_delete=models.CASCADE,null=True,blank=True,related_name='public')

class delivery_boy(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    far_id=models.ForeignKey(login,on_delete=models.CASCADE,related_name='farmer_as_table',null=True,blank=True)
    login_id=models.ForeignKey(login,on_delete=models.CASCADE,related_name='login_as_table',null=True,blank=True)


class delivery_assign(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    cart_id = models.ForeignKey(cart,on_delete=models.CASCADE,null=True,blank=True)
    delivery_team_id = models.ForeignKey(delivery_boy,on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(default=0)