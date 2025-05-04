from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from .utils import *

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

def deliver_home(request):
    return render(request ,'deliver_home.html')

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')  # Redirect to login page


def register(request):
    if request.method == 'POST':
        detl = Reg_Form(request.POST, request.FILES)
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


def deliver_register(request):
    logid=request.session.get('farmer_id')
    farid=get_object_or_404(login,id=logid)
    if request.method== 'POST':
        detl=deliver_Form(request.POST)
        paswrd=login_form(request.POST)
        if detl.is_valid() and paswrd.is_valid():
            login_data=paswrd.save(commit=False)
            login_data.user_type = 'delivery'
            login_data.save() 
            reg_data=detl.save(commit=False)
            reg_data.login_id=login_data
            reg_data.far_id=farid

            reg_data.save()
            return redirect ('farmer')
    else:
        detl=deliver_Form()
        paswrd=login_form()
    return render (request,'delivery_registration.html',{'detl':detl,'paswrd':paswrd})

def logins(request):
    if request.method == 'POST':
        form = login_verify(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = login.objects.get(email=email)
                if user.password == password:  # (Optional: Replace with check_password for security)
                    if user.user_type == 'public':
                        request.session['public_id'] = user.id
                        return redirect('public')

                    elif user.user_type == 'farmer':
                        try:
                            farmer = user.far  # using related_name='far'
                            if farmer.login_id.verification_status == 1:
                                request.session['farmer_id'] = user.id
                                return redirect('farmer')
                            elif farmer.login_id.verification_status == 0:
                                messages.error(request, 'Waiting for admin confirmation.')
                            elif farmer.login_id.verification_status == 2:
                                messages.error(request, 'Your account has been rejected by the admin.')
                            elif farmer.login_id.verification_status == 3:
                                messages.error(request, 'Your account has been frozen by the admin.')
                        except:
                            messages.error(request, 'Farmer profile not found.')

                    elif user.user_type == 'gov':
                        request.session['gov_id'] = user.id
                        return redirect('gov')

                    elif user.user_type == 'delivery':
                        request.session['deliver_id'] = user.id
                        return redirect('delivery')
                else:
                    messages.error(request, 'Invalid password')
            except login.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = login_verify()
    return render(request, 'login.html', {'form': form})


def delivery_profile_view(request):
    user_id=request.session.get('deliver_id')

    user_login_data=get_object_or_404(login,id=user_id)
    user_data=get_object_or_404(delivery_boy,login_id=user_login_data.id)

    if request.method == 'POST':
        form=deliver_Form(request.POST,instance=user_data)
        logform=login_edit_form(instance=user_login_data)
        if form.is_valid() and logform.is_valid():
            form.save()
            logform.save()
            return redirect('delivery')
    else:
        form=user_edit_form(instance=user_data)
        logform = login_edit_form(instance = user_login_data)
    return render(request,'deliver_pro.html',{'form':form,'logform':logform})

def table_view(request):
    farmer=user.objects.all()
    return render(request,'datatable.html',{'farmers' : farmer})

def public_table(request):
    pub_user=public_user.objects.all()
    return render(request,'public_data_table.html',{'publics' : pub_user})

def delivery_table(request):
    delv_user=delivery_boy.objects.all()
    return render(request,'delivery_data_table.html',{'deliverys' : delv_user})


def product_table_view(request):
    all_pro=products.objects.all().select_related('login_id__far')
    return render(request,'product_table.html',{'all_products' : all_pro})

def purchases_view(request):
    all_pro=cart.objects.all()
    return render(request,'all_purchases.html',{'all_products' : all_pro})


def comp_repporting(request,id):
    user_id=request.session.get('public_id')
    us_id=get_object_or_404(login,id=user_id)
    pro_id=get_object_or_404(products,id=id)
    if request.method=="POST":

        form=complaintform(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.userid=us_id
            comp.product_id=pro_id
            comp.save()
            return redirect('public_order_view')
    else:
        form=complaintform()
    return render(request,'complaint.html',{'form':form})


def usr_comp_view(request):
    user_id=request.session.get('public_id')
    us_id=get_object_or_404(login,id=user_id)
    us_comp=complaint.objects.filter(userid=us_id)
    
    return render(request,'complaint_view.html',{'complains':us_comp})


def editcomp(request,id):
    compl = get_object_or_404(complaint,id=id)
    if request.method == 'POST':
        form = complaintform(request.POST,instance=compl)
        if form.is_valid():
            form.save()
        return redirect('commplaint_view')
    else:
        form = complaintform(instance=compl)
    return render(request,'complaint.html',{'forms':form})


def delcomp(request,id):
    compl = get_object_or_404(complaint,id=id)
    compl.delete()
    return redirect('commplaint_view')


def far_comp_view(request):
    far_id=request.session.get('farmer_id')
    fr_id=get_object_or_404(login,id=far_id)
    compl=complaint.objects.filter(product_id__login_id=fr_id)
    return render(request,'far_complaint_view.html',{'complains':compl})

def far_comp_replay(request,id):
    far_id=request.session.get('farmer_id')
    fr_id=get_object_or_404(login,id=far_id)
    complai=complaint.objects.get(id=id )

    if request.method=="POST":

        form=replyform(request.POST)
        if form.is_valid():
            a=form.cleaned_data['reply']
            complai.reply=a
            complai.save()
            return redirect('all_complains_view')
    else:
        form=replyform()

    return render(request,'complaint_reply.html',{'form':form})

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

def payment_dtel(request,id,cartid):
    user_id=request.session.get('public_id')
    user_login_data = get_object_or_404(login,id=user_id)
    crt_id = get_object_or_404(cart,id=cartid)
    if request.method=='POST':

        payment=payment_form(request.POST)
        if payment.is_valid():

            payment_data=payment.save(commit=False)
            payment_data.login_id=user_login_data
            payment_data.cart_id=crt_id
            payment_data.save()
            # c=cart.objects.get(id=crt_id)
            # c= get_object_or_404(cart,id=cartid)
            crt_id.payment_status=1
            crt_id.save()
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

def address_add(request,id):
    user=request.session.get('public_id')
    logid=get_object_or_404(login,id=user)
    cart_id = get_object_or_404(cart,id = id )
    if request.method =="POST":
        form=address_form(request.POST)
        print(form)
        if form.is_valid():
            a = form.save(commit=False)
            a.login_id = logid
            a.save()
            return redirect('payment',a.id,cart_id.id)
    else:
        form=address_form()
        return render(request, 'public_address.html',{'form':form})
    


def all_delivery_boys(request):
    user=request.session.get('farmer_id')
    # logid=get_object_or_404(login,id=user)
    # delivery = get_object_or_404(delivery_boy,far_id = logid )
    delivery = delivery_boy.objects.filter(far_id=user)
    return render(request, 'farmer_delivery_view.html',{'delivery':delivery})

def del_cancelled(request,id):
    crt=get_object_or_404(cart,id=id)
    crt.delete()
    return redirect('public_order_view')

def ord_avil(request, id):
    farmer = request.session.get('farmer_id')
    farmer_id = get_object_or_404(login, id=farmer)
    prt = cart.objects.filter(product_id__login_id=farmer_id, payment_status=1 ,delivery_status = 0).select_related('user_id__us')
    return render(request, 'avilable_pro.html', {'prts': prt, 'delivery_id': id})


def assigning_delivery(request, id, cartid):
    cart_instance = get_object_or_404(cart, id=cartid)
    delivery_team = get_object_or_404(delivery_boy, id=id)

    if delivery_assign.objects.filter(delivery_team_id=delivery_team,status=1).exists():
        messages.error(request, 'The Delivery Boy is Busy')

    else:
        delivery_assign.objects.create(
            cart_id=cart_instance,
            delivery_team_id=delivery_team,
            status=1
        )
        cart_instance.delivery_status = 1
        cart_instance.save()
    return redirect('fa_delivery_view')

# def del_reqs(request):
#     deliv = request.session.get('deliver_id')
#     deliv_id = get_object_or_404(delivery_boy, login_id=deliv)
#     delivery_req = delivery_assign.objects.filter(delivery_team_id=deliv_id)

#     print(delivery_req)
#     # prt = cart.objects.get(id=delivery_req.cart_id)
#     return render(request, 'delivery_req.html',{'prts': delivery_req})
def del_reqs(request):
    deliv = request.session.get('deliver_id')
    deliv_id = get_object_or_404(delivery_boy, login_id=deliv)
    delivery_req = delivery_assign.objects.filter(delivery_team_id=deliv_id)
    # Attach address object to each delivery request
    for req in delivery_req:
        user = req.cart_id.user_id  # user related to the cart
        req.address = address.objects.filter(login_id=user).first()  # Get address for that user
    return render(request, 'delivery_req.html', {'prts': delivery_req})

def delevery_complete(request,id):
    # dele_boy = request.session.get('deliver_id')
    # print(dele_boy)
    deliv_id = get_object_or_404(delivery_assign, id=id)
    ad = deliv_id.cart_id.id
    deliv_id.status=0
    deliv_id.save()
    del_cart = get_object_or_404(cart,id=ad)
    del_cart.delivery_status=2
    del_cart.save()
    return redirect('delivery_request')

def farmer_approve(request,id):
    far=get_object_or_404(user,id=id)
    log_id=far.login_id
    log_id.verification_status=1
    log_id.save()
    return redirect('far-table')

def farmer_rejection(request,id):
    far=get_object_or_404(user,id=id)
    log_id=far.login_id
    log_id.verification_status=2
    log_id.save()
    return redirect('far-table')

def farmer_freez(request,id):
    far=get_object_or_404(user,id=id)
    log_id=far.login_id
    log_id.verification_status=3
    log_id.save()
    return redirect('far-table')
def gov_farmer_view(request):
    far=user.objects.all()
    return render(request,'goverment_farmer_view.html',{'farmer':far})

def gov_far_report(request,id):
    far=get_object_or_404(login,id=id)
    far.gov_status=1
    far.save()
    return redirect('gov_far_view')

def sub_purchases_view(request):
    sub_pro=farmer_cart.objects.all()
    return render(request,'sub_purchases.html',{'sub_products' : sub_pro})

CROP_SUITABILITY = {
    # Grains
    'Wheat': {'ph_range': (6.0, 7.5), 'temp_range': (10, 25), 'moisture_min': 30, 'NPK': (120, 60, 40)},
    'Rice': {'ph_range': (5.5, 7.0), 'temp_range': (20, 37), 'moisture_min': 60, 'NPK': (100, 50, 50)},
    'Maize': {'ph_range': (5.8, 7.2), 'temp_range': (18, 27), 'moisture_min': 40, 'NPK': (150, 75, 60)},
    'Barley': {'ph_range': (6.0, 8.0), 'temp_range': (12, 25), 'moisture_min': 35, 'NPK': (90, 60, 40)},
    'Millet': {'ph_range': (5.0, 7.5), 'temp_range': (20, 30), 'moisture_min': 25, 'NPK': (80, 40, 30)},

    # Vegetables
    'Tomato': {'ph_range': (5.5, 7.5), 'temp_range': (18, 27), 'moisture_min': 50, 'NPK': (120, 80, 60)},
    'Potato': {'ph_range': (5.0, 6.5), 'temp_range': (15, 25), 'moisture_min': 45, 'NPK': (100, 50, 80)},
    'Carrot': {'ph_range': (5.5, 7.0), 'temp_range': (15, 20), 'moisture_min': 40, 'NPK': (90, 50, 40)},
    'Cabbage': {'ph_range': (6.0, 7.5), 'temp_range': (15, 20), 'moisture_min': 50, 'NPK': (110, 70, 50)},
    'Spinach': {'ph_range': (6.0, 7.5), 'temp_range': (15, 25), 'moisture_min': 55, 'NPK': (100, 60, 50)},
    'Onion': {'ph_range': (6.0, 7.0), 'temp_range': (12, 24), 'moisture_min': 30, 'NPK': (80, 50, 40)},
    
    # Fruits
    'Apple': {'ph_range': (5.0, 6.5), 'temp_range': (15, 25), 'moisture_min': 60, 'NPK': (90, 60, 80)},
    'Banana': {'ph_range': (5.5, 7.0), 'temp_range': (22, 30), 'moisture_min': 75, 'NPK': (200, 80, 250)},
    'Mango': {'ph_range': (5.5, 7.5), 'temp_range': (24, 30), 'moisture_min': 50, 'NPK': (150, 100, 150)},
    'Strawberry': {'ph_range': (5.5, 6.5), 'temp_range': (15, 22), 'moisture_min': 60, 'NPK': (100, 50, 60)},
    'Pineapple': {'ph_range': (4.5, 6.5), 'temp_range': (22, 32), 'moisture_min': 65, 'NPK': (120, 80, 100)},
    'Grapes': {'ph_range': (5.5, 7.0), 'temp_range': (20, 30), 'moisture_min': 40, 'NPK': (90, 60, 50)},

    # Pulses (Legumes)
    'Lentils': {'ph_range': (6.0, 7.5), 'temp_range': (15, 25), 'moisture_min': 35, 'NPK': (50, 40, 30)},
    'Chickpeas': {'ph_range': (5.5, 7.0), 'temp_range': (15, 25), 'moisture_min': 30, 'NPK': (60, 40, 50)},
    'Peas': {'ph_range': (6.0, 7.5), 'temp_range': (12, 22), 'moisture_min': 45, 'NPK': (70, 40, 60)},
    'Beans': {'ph_range': (6.0, 7.5), 'temp_range': (15, 25), 'moisture_min': 40, 'NPK': (80, 50, 70)},

    # Cash Crops
    'Sugarcane': {'ph_range': (6.5, 7.5), 'temp_range': (21, 30), 'moisture_min': 50, 'NPK': (150, 80, 100)},
    'Cotton': {'ph_range': (5.8, 8.0), 'temp_range': (21, 30), 'moisture_min': 35, 'NPK': (120, 60, 90)},
    'Tea': {'ph_range': (4.5, 6.0), 'temp_range': (20, 30), 'moisture_min': 60, 'NPK': (110, 90, 70)},
    'Coffee': {'ph_range': (5.5, 6.5), 'temp_range': (18, 24), 'moisture_min': 50, 'NPK': (120, 80, 90)},

    # Nuts
    'Peanuts': {'ph_range': (5.5, 7.0), 'temp_range': (22, 30), 'moisture_min': 30, 'NPK': (60, 40, 70)},
    'Almonds': {'ph_range': (6.0, 7.5), 'temp_range': (18, 30), 'moisture_min': 25, 'NPK': (80, 50, 60)},
    'Cashew': {'ph_range': (5.0, 6.5), 'temp_range': (24, 32), 'moisture_min': 40, 'NPK': (70, 50, 60)},

    # Root Crops
    'Sweet Potato': {'ph_range': (5.5, 6.5), 'temp_range': (21, 29), 'moisture_min': 50, 'NPK': (80, 40, 70)},
    'Yam': {'ph_range': (5.0, 6.5), 'temp_range': (22, 30), 'moisture_min': 55, 'NPK': (90, 50, 80)},

    # Herbs
    'Basil': {'ph_range': (6.0, 7.5), 'temp_range': (18, 30), 'moisture_min': 40, 'NPK': (60, 40, 50)},
    'Mint': {'ph_range': (5.5, 7.5), 'temp_range': (15, 30), 'moisture_min': 50, 'NPK': (70, 50, 60)},
    'Coriander': {'ph_range': (6.2, 6.8), 'temp_range': (17, 27), 'moisture_min': 45, 'NPK': (50, 40, 60)},
}

def check_suitable_crops(data):
    crop_results = []

    for crop, conditions in CROP_SUITABILITY.items():
        ph_min, ph_max = conditions['ph_range']
        temp_min, temp_max = conditions['temp_range']
        moisture_min = conditions['moisture_min']
        ideal_n, ideal_p, ideal_k = conditions.get('NPK', (0, 0, 0))

        if (ph_min <= data['ph'] <= ph_max and
            temp_min <= data['temperature'] <= temp_max and
            data['moisture'] >= moisture_min and
            data['nitrogen'] >= ideal_n and
            data['phosphorus'] >= ideal_p and
            data['potassium'] >= ideal_k):

            # Simple yield estimation (out of 100)
            yield_score = 100

            # PH penalty
            ph_ideal = (ph_min + ph_max) / 2
            yield_score -= abs(data['ph'] - ph_ideal) * 5

            # Temperature penalty
            temp_ideal = (temp_min + temp_max) / 2
            yield_score -= abs(data['temperature'] - temp_ideal) * 2

            # Moisture penalty
            yield_score -= max(0, (moisture_min - data['moisture']) * 1.5)

            # NPK penalty
            yield_score -= abs(data['nitrogen'] - ideal_n) * 0.1
            yield_score -= abs(data['phosphorus'] - ideal_p) * 0.1
            yield_score -= abs(data['potassium'] - ideal_k) * 0.1

            yield_score = max(0, round(yield_score))  # Clamp to 0+

            crop_results.append({'name': crop, 'estimated_yield': yield_score})

    return crop_results



def enter_soil_data(request):
    form = SoilDataForm()
    crop_results = None

    if request.method == "POST":
        form = SoilDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            crop_results = check_suitable_crops(data)
    
    return render(request, 'soil_data.html', {'form': form, 'crop_results': crop_results})

from django.http import JsonResponse
import requests


from django.http import JsonResponse
import requests

API_KEY = "373bb983b7f2afba905fd40bb214ed15"  # Replace with your OpenWeatherMap API key

#import requests
from django.http import JsonResponse

# API_KEY = "your_new_api_key"

def get_weather(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({"error": "Latitude or longitude missing"}, status=400)

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    uv_url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        # Get weather data
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Get UV index data
        uv_response = requests.get(uv_url)
        uv_response.raise_for_status()
        uv_data = uv_response.json()

        # Prepare response
        weather_info = {
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "weather": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"],
            "uv_index": uv_data.get("value", "N/A")  # UV index may not always be available
        }

        return JsonResponse(weather_info)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Weather API error: {str(e)}"}, status=500)


def weather(request):
    return render(request, 'liveweather.html')

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def upload_image(request):
    if request.method == 'POST':
        form = LeafImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']  # Get uploaded file
            file_path = os.path.join('media/uploads', image_file.name)  # Save path

            # Save file manually
            file_name = default_storage.save(file_path, ContentFile(image_file.read()))

            # Get full path
            full_file_path = default_storage.path(file_name)

            # Predict disease
            prediction = predict_disease(full_file_path)
            fertilizer = DISEASE_FERTILIZER_MAPPING.get(prediction, "No specific fertilizer recommendation.")

            return render(request, 'upload.html', {'form': form, 'prediction': prediction, 'fertilizer': fertilizer})

    else:
        form = LeafImageForm()
    
    return render(request, 'upload.html', {'form': form})