from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('farmer/', views.farmer_home, name='farmer'),
    path('', views.landing_page, name='index'),
    path('admins/', views.admin_page, name='admins'),
    path('login/', views.logins, name='login'),
    path('register/', views.register, name='register'),
    path('table/', views.table_view, name='table'),
    path('profile/',views.profile_view,name='profile'),
    path('public_profile_view/',views.public_profile_view,name='public_profile_view'),
    path('public_register/', views.public_register, name='public_register'),
    path('product_view/', views.product_view, name='product_view'),
    path('add_pro/', views.product_add, name='add_pro'),
    path('del_pro/<int:id>/',views.product_del,name='del_pro'),
    path('public/', views.public_home, name='public'),
    path('public_pro_view/', views.public_pro_view, name='public_pro_view'),
    path('edit_pro/<int:id>/',views.product_edit,name='edit_pro'),
    path('cart/<int:p_id>/',views.add_to_cart,name='cart'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('cart_del/<int:id>/',views.cart_product_del,name='cart_del'),
    path('payment/<int:id>/',views.payment_dtel,name='payment'),
    path('order_view/',views.farmer_order_view,name='order_view'),
    path('public_order_view/',views.my_order,name='public_order_view'),
    path('order_cancel/<int:id>/',views.my_order_cancel,name='order_cancel'),
    path('alert',views.alert_add,name='alert'),
    path('ad_alert_view',views.admin_alert_view,name='ad_alert_view'),
    path('alert_edit/<int:id>/',views.edit_alert,name='alert_edit'),
    path('alert_del/<int:id>/',views.del_alert,name='alert_del'),
    path('far_alert_view/',views.fa_alert_view,name='far_alert_view')

    
    
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)