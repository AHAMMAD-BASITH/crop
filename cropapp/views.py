from django.shortcuts import render,redirect,get_object_or_404
from .models import login,user,public_user,products,cart
from .forms import Reg_Form,login_form,login_verify,user_edit_form,login_edit_form,public_Form,products_form
from django.contrib import messages

# Create your views here.

def farmer_home(request):
    return render( request ,'farmer_home.html')

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
            login_data=paswrd.save()
            reg_data=detl.save(commit=False)
            reg_data.login_id=login_data
            reg_data.save()
            return redirect ('/user')
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
            return redirect ('public')
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
    return render(request,'edit.html',{'form':form,'logform':logform})


def product_add(request):
    user_id=request.session.get('id')
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
    user_id=request.session.get('id')
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
    u_id=request.session.get('id')
    user_login_data = get_object_or_404(login, id=u_id)
    product=get_object_or_404(products, id=p_id)
    print(user_login_data)
    print(product)
    if cart.objects.filter(product_id=product,user_id=user_login_data).exists():
        messages.success(request,'product already exists')
    else:
        cart_data = cart.objects.create(
            product_id = product,
            user_id = user_login_data
        )
    return redirect('public_pro_view')

