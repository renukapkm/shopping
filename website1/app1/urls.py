from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('services',views.services,name='services'),
    path('contact',views.contact,name='contact'),
    path('product',views.product,name='product'),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('cart',views.cart,name='cart'),
    path('categary',views.categary,name='categary'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('editcategary/<int:id>',views.editcategary,name='editcategary'),
    path('checkout',views.checkout,name='checkout'),
    path('myorders',views.myorders,name='myorders'),
    path('confirmorder',views.confirmorder,name='confirmorder'),
    path('account',views.account,name='account'),
    path('addtowish/<int:id>',views.addtowish,name='addtowish'),
    path('registration',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('wish',views.wish,name='wish'),
    




# admin pages

    path('dashboard',views.dashboard,name='dashboard'),
    path('contacts',views.contacts,name='contacts'),
    path('dashregistration',views.dashregistration,name='dashregistration'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addcategary',views.addtocategary,name='addcategary'),
    path('admincategary',views.admincategary,name='admincategary'),
    path('adminproducts',views.adminproducts,name='adminproducts'),
    path('addnotifications',views.addnotifications,name='addnotifications'),
    path('dashboardlogin',views.dashboardlogin,name='dashboardlogin'),
    path('dashlogout',views.dashlogout,name='dashlogout'),


]

urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT) 