from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def farmer_home(request):
    return render( request ,'farmer_home.html')

def gov_home(request):
    return render( request ,'gov_home.html')

def landing_page(request):
    return render( request ,'index.html')

def admin_page(request):
    return render( request ,'admin.html')

def login_page(request):
    return render( request ,'login.html')

def public_home(request):
    return render( request ,'public.html')



def register(request):
    if request.method == 'POST':
        detl=Reg_Form(request.POST)
        paswrd=login_form(request.POST)
        if detl.is_valid() and paswrd.is_valid():
            login_data=paswrd.save(commit=False)
            login_data.user_type = 'farmer'
            login_data.save()
            reg_data=detl.save(commit=False)
            reg_data.login_id=login_data
            reg_data.save()
            return redirect ('login')
    else:
        detl=Reg_Form()
        paswrd=login_form()
    return render (request,'register.html',{'detl':detl,'paswrd':paswrd})

def public_register(request):
    if request.method == 'POST':
        detl=public_Form(request.POST)
        paswrd=login_form(request.POST)
        if detl.is_valid() and paswrd.is_valid():
            login_data=paswrd.save(commit=False)
            login_data.user_type = 'public'
            login_data.save() 
            reg_data=detl.save(commit=False)
            reg_data.login_id=login_data

            reg_data.save()
            return redirect ('login')
    else:
        detl=public_Form()
        paswrd=login_form()
    return render (request,'public_registration.html',{'detl':detl,'paswrd':paswrd})


def logins(request):
    if request.method =='POST':
        form=login_verify(request.POST)
        if form.is_valid():
            email =form.cleaned_data['email']
            password =form.cleaned_data['password']
            try:
                user = login.objects.get(email=email)
                if user.password == password:
                    if user.user_type=='public':
                        request.session['public_id']=user.id
                        return redirect('public')
                    elif user.user_type=='farmer':
                        request.session['farmer_id']=user.id
                        return redirect('farmer')
                    elif user.user_type=='gov':
                        request.session['gov_id']=user.id
                        return redirect('gov')
                else:
                    messages.error(request, 'Invalid password')
            except login.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = login_verify()
    return render(request,'login.html',{'form':form})

def table_view(request):
    farmer=user.objects.all()
    return render(request,'datatable.html',{'farmers' : farmer})


def usre_edit(request,id):
    user = get_object_or_404(login,id=id)
    if request.method == 'POST':
        form = Reg_Form(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userData')
    else:
        form=Reg_Form(instance=user)
    return render(request,'edit_page.html',{'form':form})

def profile_view(request):
    # user = get_object_or_404(login,id=id)
    user_id=request.session.get('farmer_id')
    user_login_data = get_object_or_404(login,id=user_id)
    user_data = get_object_or_404(user,login_id=user_login_data)

    if request.method == 'POST':
        form = user_edit_form(request.POST,instance=user_data)
        logform=login_edit_form(request.POST,instance=user_login_data)
        if form.is_valid() and logform.is_valid():
            form.save()
            logform.save()
            return redirect('farmer')
    else:
        form=user_edit_form(instance=user_data)
        logform = login_edit_form(instance = user_login_data)
    return render(request,'edit.html',{'form':form,'logform':logform})


def public_profile_view(request):
    # user = get_object_or_404(login,id=id)
    user_id=request.session.get('public_id')
    user_login_data = get_object_or_404(login,id=user_id)
    user_data = get_object_or_404(public_user,login_id=user_login_data)

    if request.method == 'POST':
        form = public_Form(request.POST,instance=user_data)
        logform=login_edit_form(request.POST,instance=user_login_data)
        if form.is_valid() and logform.is_valid():
            form.save()
            logform.save()
            return redirect('public')
    else:
        form=user_edit_form(instance=user_data)
        logform = login_edit_form(instance = user_login_data)
    return render(request,'public_pro_edit.html',{'form':form,'logform':logform})


def product_add(request):
    user_id=request.session.get('farmer_id')
    user_login_data = get_object_or_404(login,id=user_id)
    if request.method=='POST':

        product=products_form(request.POST,request.FILES)
        if product.is_valid():

            pro_data=product.save(commit=False)
            pro_data.login_id=user_login_data
            pro_data.save()
            return redirect('product_view')
    else:
        product=products_form()
    return render(request,'products.html',{'product':product})

def product_view(request):
    user_id=request.session.get('farmer_id')
    user_login_data = get_object_or_404(login,id=user_id)
    all_product=products.objects.filter(login_id=user_login_data)
    return render(request,'product_view.html',{'all_products' : all_product})

def product_del(request,id):
    product=get_object_or_404(products,id=id)
    product.delete()
    return redirect('product_view')

def product_edit(request,id):
    product=get_object_or_404(products,id=id)
    if request.method=='POST':
        form=products_form(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
        return redirect('product_view')
    else:
        form=products_form(instance=product)
    return render(request ,'product_edit.html',{'product' : form})

def public_pro_view(request):
    all_product=products.objects.all()
    return render(request,'public_product_view.html',{'all_products' : all_product})

def add_to_cart(request,p_id):
    u_id=request.session.get('public_id')
    user_login_data = get_object_or_404(login, id=u_id)
    product=get_object_or_404(products, id=p_id)
    if cart.objects.filter(product_id=product,user_id=user_login_data,cancelation_status=0).exists():
        messages.success(request,'product already exists')
    else:
        cart_data = cart.objects.create(
            product_id = product,
            user_id = user_login_data
        )
    return redirect('public_pro_view')

def cart_view(request):
    user_id=request.session.get('public_id')
    user_login_data = get_object_or_404(login,id=user_id)
    cart_product=cart.objects.filter(user_id=user_login_data,payment_status=0)
    return render(request,'cart.html',{'cart_products' : cart_product})


def cart_product_del(request,id):
    cart_product=get_object_or_404(cart,id=id)
    cart_product.delete()
    return redirect('cart_view')

def payment_dtel(request,id):
    user_id=request.session.get('public_id')
    user_login_data = get_object_or_404(login,id=user_id)
    crt_id = get_object_or_404(cart,id=id)
    if request.method=='POST':

        payment=payment_form(request.POST)
        if payment.is_valid():

            payment_data=payment.save(commit=False)
            payment_data.login_id=user_login_data
            payment_data.cart_id=crt_id
            payment_data.save()
            # c=cart.objects.get(id=crt_id)
            c= get_object_or_404(cart,id=id)
            c.payment_status=1
            c.save()
            return redirect('cart_view')
    else:
        payment=payment_form()

    return render( request ,'payment.html',{'payment':payment})

def my_order(request):
    user=request.session.get('public_id')
    users_id = get_object_or_404(login,id=user)
    myord = cart.objects.filter(user_id=users_id,payment_status=1)
    return render(request,'my_orders.html',{'myords':myord})


def farmer_order_view(request):
    farmer = request.session.get('farmer_id')
    farmer_id = get_object_or_404(login, id=farmer)
    prt = cart.objects.filter(product_id__login_id=farmer_id, payment_status=1).select_related('user_id__us')
    return render(request, 'farmer_order_view.html', {'prts': prt})


def my_order_cancel(request,id):
    user=request.session.get('public_id')
    users_id = get_object_or_404(login,id=user)
    crt_id = get_object_or_404(cart,id=id)
    crt_id.cancelation_status=1
    crt_id.save()
    return redirect('public_order_view')


def alert_add(request):
    if request.method == "POST":
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ad_alert_view')  
    else:
        form = AlertForm()
    return render(request, 'add_alert.html', {'form': form})

def admin_alert_view(request):
    alerts = alert.objects.all()
    return render(request, 'admin_alert_view.html',{'alerts':alerts})


def edit_alert(request,id):
    alerts = get_object_or_404(alert,id=id)
    if request.method == 'POST':
        form = AlertForm(request.POST,instance=alerts)
        if form.is_valid():
            form.save()
        return redirect('ad_alert_view')
    else:
        form = AlertForm(instance=alerts)
    return render(request,'edit_alert.html',{'forms':form})

def del_alert(request,id):
    alerts=get_object_or_404(alert,id=id)
    alerts.delete()
    return redirect('ad_alert_view')

def fa_alert_view(request):
    alerts = alert.objects.all().order_by('-created_at')
    return render(request, 'farmer_alert_view.html', {'alerts': alerts})


def gov_product_add(request):
    if request.method=='POST':

        product=gov_products_form(request.POST,request.FILES)
        if product.is_valid():
            product.save()
            return redirect('gov_view_pro')
    else:
        product=gov_products_form()
    return render(request,'gov_prod_add.html',{'product':product})

def gov_product_view(request):
    gov_product=gov_products.objects.all()
    return render(request,'gov_product_view.html',{'gov_product':gov_product})

def gov_pro_edit(request,id):
    products=get_object_or_404(gov_products,id=id)
    if request.method=='POST':
        form=gov_products_form(request.POST,request.FILES,instance=products)
        if form.is_valid():
            form.save()
        return redirect('gov_view_pro')
    else:
        form=gov_products_form(instance=products)
    return render(request ,'gov_prod_edit.html',{'product' : form})

def del_gov_pro(request,id):
    gov_pro=get_object_or_404(gov_products,id=id)
    gov_pro.delete()
    return redirect('gov_view_pro')


def far_subsidy_view(request):
    all_product=gov_products.objects.all()
    return render(request,'farmer_product_view.html',{'all_products' : all_product})

def f_add_to_cart(request,id):
    f_id=request.session.get('farmer_id')
    farmer_login_data = get_object_or_404(login, id=f_id)
    product=get_object_or_404(gov_products, id=id)
    if farmer_cart.objects.filter(product_id=product,user_id=farmer_login_data,cancelation_status=0).exists():
        messages.success(request,'product already exists')
    else:
        cart_data = farmer_cart.objects.create(
            product_id = product,
            user_id =farmer_login_data
        )
    return redirect('frmr_pro_view')

def far_cart_view(request):
    far_id=request.session.get('farmer_id')
    user_login_data = get_object_or_404(login,id=far_id)
    cart_product=farmer_cart.objects.filter(user_id=user_login_data,payment_status=0)
    return render(request,'frmr_pro_view.html',{'cart_products' : cart_product})


def cart_product_del(request,id):
    cart_product=get_object_or_404(farmer_cart,id=id)
    cart_product.delete()
    return redirect('cart_view')

def far_payment_dtel(request,id):
    far_id=request.session.get('farmer_id')
    farmer_login_data = get_object_or_404(login,id=far_id)
    crt_id = get_object_or_404(farmer_cart,id=id)
    if request.method=='POST':

        payment=farmer_payment_form(request.POST)
        if payment.is_valid():

            payment_data=payment.save(commit=False)
            payment_data.login_id=farmer_login_data
            payment_data.cart_id=crt_id
            payment_data.save()
            # c=cart.objects.get(id=crt_id)
            c= get_object_or_404(farmer_cart,id=id)
            c.payment_status=1
            c.save()
            return redirect('frmr_pro_view')
    else:
        payment=farmer_payment_form()

    return render( request ,'farmer_payment.html',{'payment':payment})

def far_order(request):
    far=request.session.get('farmer_id')
    far_id = get_object_or_404(login,id=far)
    myord = farmer_cart.objects.filter(user_id=far_id,payment_status=1)
    return render(request,'far_my_orders.html',{'myords':myord})

def far_order_cancel(request,id):
    far=request.session.get('farmer_id')
    far_id = get_object_or_404(login,id=far)
    crt_id = get_object_or_404(farmer_cart,id=id)
    crt_id.cancelation_status=1
    crt_id.save()
    return redirect('farmer_order_view')


def gov_orders(request):
    prt = farmer_cart.objects.filter( payment_status=1).select_related('user_id__us')
    return render(request, 'gov_orders_views.html', {'prts': prt})


def notification_add(request):
    if request.method == "POST":
        form = NotificatioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gov_notify_view')  
    else:
        form = NotificatioForm()
    return render(request, 'add_notification.html', {'form': form})

def gov_notification_view(request):
    alerts = notification.objects.all()
    return render(request, 'gov_notification_view.html',{'alerts':alerts})


def edit_notification(request,id):
    alerts = get_object_or_404(notification,id=id)
    if request.method == 'POST':
        form = NotificatioForm(request.POST,instance=alerts)
        if form.is_valid():
            form.save()
        return redirect('gov_notify_view')
    else:
        form = NotificatioForm(instance=alerts)
    return render(request,'notification_edit.html',{'forms':form})

def del_notification(request,id):
    alerts=get_object_or_404(notification,id=id)
    alerts.delete()
    return redirect('gov_notify_view')

def fa_notification_view(request):
    alerts = notification.objects.all().order_by('-created_at')
    return render(request, 'farmer_notification_view.html', {'alerts': alerts})