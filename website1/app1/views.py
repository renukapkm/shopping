from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from django.template import loader
from .models import Contact
from.models import Registration
from.models import Product
from.models import Cart
from.models import Catergary
from.models import Order
from.models import Wishlist , Notification,Dashregistration
import datetime




# Create your views here.
def index(request):
    cat = Catergary.objects.all().values()
    pro = Product.objects.all()
    wish=Wishlist.objects.all().values()
    noty=Notification.objects.all()
    context={
        'cat':cat,
        'pro':pro,
        'wish':wish,
        'noty':noty,
    }
    template=loader.get_template("index.html")
    return HttpResponse(template.render(context,request))
def about(request):
    template=loader.get_template("about.html")
    return HttpResponse(template.render({},request))
def services(request):
    template=loader.get_template("services.html")
    return HttpResponse(template.render({},request))


def product(request):
    cat = Catergary.objects.all().values()
    if 'catid' in request.GET:
        catid =request.GET['catid']
        pro = Product.objects.filter(procat_id=catid)
    else:
        pro = Product.objects.all()
    context = {
        'pro':pro,
        'cat':cat,
    }

    template=loader.get_template("product.html")
    return HttpResponse(template.render(context,request))
def categary(request):
    cat = Catergary.objects.all().values()
    context ={
        'cat':cat
    }
    template=loader.get_template("categary.html")
    return HttpResponse(template.render(context,request))

def addtocategary(request):
    if request.method == 'POST':
        catename = request.POST['cate_name']
       
        cateimage = request.FILES['cate_image']

        cate = Catergary( cate_name =catename , cate_image = cateimage)
        
        cate.save()

    template=loader.get_template("dashboard/addcategary.html")  
    return HttpResponse(template.render({},request))


def addtocart(request,id):
    # cartcount = 0
    
    if "user" not in request.session:
        return HttpResponseRedirect("/login")
    
 
    exits = Cart.objects.filter(cart_proid=id , cart_user = request.session["user"])
    if exits:
       exits = Cart.objects.filter(cart_proid=id , cart_user = request.session["user"])[0]
       exits.cart_qty +=1
       exits.cart_amount = exits.cart_qty = exits.cart_price
       exits.save()
    else:
        pro = Product.objects.filter(id=id)[0]
        cart = Cart(cart_user = request.session["user"],
                    cart_proid= pro.id, cart_name =pro.pro_name , 
                    cart_price =pro.pro_price, cart_image = pro.pro_image,cart_qty = 1,cart_amount = pro.pro_price)
        cart.save()
        user =request.session["user"]
        # cartcount = 0    
        cart1 =Cart.objects.filter( cart_user =user)
        cartcount = cart1.count()
        request.session["cart"]= cartcount
        
    return HttpResponseRedirect("/cart")
 
def cart(request):
    if  'user' not in request.session:
        return HttpResponseRedirect('/login')
    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)
        delcart.delete()
        user =request.session["user"]
        # cartcount = 0    
        cart1 =Cart.objects.filter( cart_user =user)
        cartcount = cart1.count()
        request.session["cart"]= cartcount
        return HttpResponseRedirect('/cart')
        # change cart quantity

    if 'q' in request.GET:
        q =request.GET['q']
        s= request.GET['s']
        cart3 = Cart.objects.filter(id=s)[0]
        if q =='inc':
            cart3.cart_qty+=1
        elif q == 'dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1
        cart3.cart_amount = cart3.cart_qty * cart3.cart_price
        cart3.save()

    user = request.session["user"]
    cart = Cart.objects.filter(cart_user = user).values()
    cart2 = Cart.objects.filter(cart_user = user)
    tot=shp=gst=gtot=0
    for x in cart2:
        tot+= x.cart_amount
        shp = tot *10/100
        gst = tot *18/100
        gtot = tot+shp+gst

        request.session['tot']=tot
        request.session['shp']=shp
        request.session['gst']=gst
        request.session['gtot']=gtot




    context = {
            'cart' : cart,
            'tot'  : tot,
            'shp'  : shp,
            'gst'   : gst,
            'gtot' : gtot
        }
    template=loader.get_template("cart.html")
    return HttpResponse(template.render(context,request))

def contact(request):
    if request.method == 'POST':
        cname = request.POST['contact_name']
        cemail = request.POST['contact_email']
        cmsg = request.POST['contact_message']

        con = Contact(con_name = cname,con_email = cemail,con_message = cmsg)
        con.save()

    template=loader.get_template("contact.html")
    return HttpResponse(template.render({},request))


def registration(request):
    if "user" in request.session:
        return HttpResponseRedirect("/account")
    if request.method == 'POST':
        # regname = request.POST['reg_name']
        regemail = request.POST['reg_email']
        regpassword = request.POST['reg_passwd']
        reguser = request.POST['reg_usrname']
        regphnumber = request.POST['reg_ph']
        regname = request.POST['reg_name']



        regi = Registration(reg_email = regemail,reg_password = regpassword,reg_username = reguser,reg_phnum = regphnumber,reg_name=regname)  
        regi.save()

    template=loader.get_template("registration.html")
    return HttpResponse(template.render({},request))

def login(request):
    cartcount=0
    if "user" in request.session:
        return HttpResponseRedirect("/account")
    if request.method == 'POST':
        log_user = request.POST['log_user']
        
        log_pass = request.POST['log_passwd']

        log = Registration.objects.filter(reg_username = log_user,reg_password=log_pass)
        if log:
            request.session["user"] = log_user
            user =request.session["user"]
    
            cart =Cart.objects.filter( cart_user =user)
            cartcount = cart.count()
            request.session["cart"]=cartcount

            wish =Wishlist.objects.filter( wish_user =user)
            wishcount = wish.count()
            request.session["wish"]=wishcount

            user =request.session["user"]
    
            noty =Notification.objects.all()
            notycount = noty.count()
            request.session["noty"]=notycount
           
            return HttpResponseRedirect("/account?home")
        
    template=loader.get_template("login.html")
    return HttpResponse(template.render({},request))


def logout(request):
    if "user" in request.session:
        del request.session["user"]
        return HttpResponseRedirect("/login")
    



    # dashboard
def dashboardlogin(request):
    
    if "adminuser" in request.session:
        return HttpResponseRedirect("/account")
    if request.method == 'POST':
        log_user = request.POST['log_user']
        
        log_pass = request.POST['log_passwd']

        log = Dashregistration.objects.filter(dash_username = log_user,dash_password=log_pass)
        if log:
            request.session["adminuser"] = log_user
           
            return HttpResponseRedirect("/dashboard")
        
    template=loader.get_template("dashboard/dashboardlogin.html")
    return HttpResponse(template.render({},request))


def dashlogout(request):
    if "adminuser" in request.session:
        del request.session["adminuser"]
        return HttpResponseRedirect("/dashboardlogin")
    


        
def dashboard(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    
    template=loader.get_template("dashboard/dashboard.html")  
    return HttpResponse(template.render({},request)) 
def contacts(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    cons = Contact.objects.all().values()
    context = {
        'contacts':cons
    }
    template=loader.get_template("dashboard/contacts.html")  
    return HttpResponse(template.render(context,request))


   
def dashregistration(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    dashreg = Registration.objects.all().values()
    context = {
        'dashregistration':dashreg 
    }
    template=loader.get_template("dashboard/dashregistration.html")  
    return HttpResponse(template.render(context,request))




# product page

def addproduct(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    if request.method == 'POST':
        proname = request.POST['pro_name']
        proprice = request.POST['pro_price']
        proimage = request.FILES['pro_image']
        procat = request.POST['cat']

        prod = Product( pro_name =proname ,pro_price = proprice, pro_image = proimage,procat_id = procat)
        
        prod.save()
    catt = Catergary.objects.all().values()
    context = {
            'catt':catt
           }
        


    template=loader.get_template("dashboard/addproduct.html")  
    return HttpResponse(template.render(context,request))

def adminproducts(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    ap = Product.objects.all()
    catnames =[]
    for x in ap:
        catid = x.procat_id
        cat = Catergary.objects.filter(id =  catid)[0]
        catnames.append(cat.cate_name)
    context = {
        'ap': zip(ap,catnames)
        
    }
    if 'del' in request.GET:
        id = request.GET['del']
        delpro = Product.objects.filter(id=id)[0]
        delpro.delete()
        return HttpResponseRedirect("/adminproducts")
    template=loader.get_template("dashboard/adminproducts.html")  
    return HttpResponse(template.render(context,request))


def admincategary(request):
    if "adminuser" not in request.session:
        return HttpResponseRedirect("/dashboardlogin")
        
    admincate = Catergary.objects.all()
    if 'del' in request.GET:
        id = request.GET['del']
        delcate = Catergary.objects.filter(id=id)[0]
        delcate.delete()
        return HttpResponseRedirect("/adminproducts")
    context = {
        'admincate':admincate
    }

    template=loader.get_template("dashboard/admincategary.html")  
    return HttpResponse(template.render(context,request))
def edit(request,id):
    w=Product.objects.filter(id=id)[0]
    if request.method =="POST":
        name = request.POST['pro_name']
        price = request.POST['pro_price']
        updatepro=Product.objects.filter(id=id)[0]
        updatepro.pro_name=name
        updatepro.pro_price=price
        if len(request.FILES) !=0:
            image=request.FILES['pro_image']
            updatepro.pro_image=image
        updatepro.save()
        
        return HttpResponseRedirect("/adminproducts")
    context = {
        'w':w,
        
    }

    template=loader.get_template("dashboard/edit.html")  
    return HttpResponse(template.render(context,request))

def editcategary(request,id):
    category=Catergary.objects.filter(id=id).values()
    if request.method == "POST":
        editname=request.POST['cate_name']

        updatecate=Catergary.objects.filter(id=id)[0]
        updatecate.cate_name=editname
        if len(request.FILES) !=0:
            editimage=request.FILES['cate_image']

            updatecate.cate_image=editimage
        updatecate.save()
        return HttpResponseRedirect("/admincategary")
    context = {
        'category':category,
        
    }

    template=loader.get_template("dashboard/editcategary.html")  
    return HttpResponse(template.render(context,request))


def checkout(request):
    if 'user'  not in request.session:
        return HttpResponseRedirect('/login')
    co=0
    adrs=dtype = ""

    # after order submit

    if 'dlv_adrs' in request.POST:
        adrs = request.POST["dlv_adrs"]
        dtype = request.POST["dlv_type"]
        co=1
    user = request.session["user"]

    # delete old data from order
    oldoder = Order.objects.filter(order_user =user,order_status=0) 
    oldoder.delete()


    # add cart data to order table

    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr=Order(order_user = x.cart_user,order_name = x.cart_name,order_price= x.cart_price,
                  order_image=x.cart_image,order_qty=x.cart_qty,order_amount=x.cart_amount,
                  order_address=adrs,order_dlvtype=dtype,
                  order_status=0)
        odr.save()  

# display order status
    order=Order.objects.filter(order_user = user,order_status=0).values()

    tot=request.session["tot"]
    gst=request.session['gst']
    shp=request.session['shp']
    gtot=request.session['gtot']
    
    context={
        'order':order,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot,
        'co':co
    }
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))
def confirmorder(request):
    user = request.session["user"]
    order = Order.objects.filter( order_user=user,order_status=0)
    for x in order:
        x.order_status=1
        x.save()

    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))

def myorders(request):
    user = request.session["user"]
    order = Order.objects.filter(order_user=user,order_status=1)
    context = {
        'order':order

    }

    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))

def account(request):
    if "user" not in request.session:
        return HttpResponseRedirect("/login")
    order =''
    pro=''
    wish =''
    noti=''
    ordercount = 0
    wishorder = 0
    user =request.session["user"]
    if request.method == 'POST':
        rname=request.POST['profile_name']
        remail=request.POST['profile_email']
        # regimg=request.POST['profile_img']
        # regpasswd=request.POST['profile_password']
        reg=Registration.objects.filter( reg_username = user)[0]

        reg.reg_name=rname
        reg.reg_email=remail
        # reg.reg_password=regpasswd
        if len(request.FILES) !=0:
           regimg=request.FILES['profile_img']
           reg.reg_img=regimg
      
        # reg.reg_img=regimg
           
        reg.save()
        # it is used in re direct same page use this code
        return HttpResponseRedirect("/account?pro")

    if 'ord' in request.GET:
       user =request.session["user"] 
       order =Order.objects.filter( order_user =user)
       ordercount = order.count()
    elif 'pro' in request.GET:
        user =request.session["user"] 
        pro=Registration.objects.filter(reg_username=user)
    elif 'wish' in request.GET:
        user =request.session["user"]
        wish=Wishlist.objects.filter(wish_user=user)
        wishorder = wish.count()
    elif 'noti' in request.GET:
        user=request.session["user"]
        noti=Notification.objects.all()
    acc = Registration.objects.filter(reg_username = user)
    context ={
        'acc':acc,
        'order':order,
        'pro':pro,
        'wish':wish,
        'noti':noti,
        'ordercount':ordercount,
        'wishorder':wishorder,
        

    }
    template=loader.get_template("account.html")
    return HttpResponse(template.render(context,request))
def wish(request):
    if  'user' not in request.session:
        return HttpResponseRedirect('/login')
    if 'del' in request.GET:
        id = request.GET['del']
        delwish = Wishlist.objects.filter(id=id)
        delwish.delete()
        user =request.session["user"]
    
        wish =Wishlist.objects.filter( wish_user =user)
        wishcount = wish.count()
        request.session["wish"]=wishcount
       
    user = request.session["user"]
    wish = Wishlist.objects.filter(wish_user = user).values()
   
    context = {
            'wish' : wish,
                    }
    template=loader.get_template("wish.html")
    return HttpResponse(template.render(context,request))
    
 


def addtowish(request,id):
    wishcount=0
    if 'user' not in request.session:
        return HttpResponseRedirect("/login")
    exist = Wishlist.objects.filter(wish_proid=id, wish_user = request.session["user"])
    if exist:
        HttpResponseRedirect("/wish")
    else:
        pro=Product.objects.filter(id=id)[0]
        wish =Wishlist(wish_user =request.session["user"],
                       wish_proid= pro.id,
                       wish_name = pro.pro_name,wish_price =pro.pro_price,wish_image=pro.pro_image)
        wish.save()
        user =request.session["user"]
    
        wish =Wishlist.objects.filter( wish_user =user)
        wishcount = wish.count()
        request.session["wish"]=wishcount
       

    
    return HttpResponseRedirect("/wish")

def addnotifications(request):
    if 'user' not in request.session:
        return HttpResponseRedirect("/login")
    
    if request.method == 'POST':
        notify = request.POST["notify"]
        # date = request.POST["date"]
        date= datetime.datetime.now()
        
        noti = Notification(noti_message =notify, noti_date=date)

        noti.save()
        user =request.session["user"]
    
        noty =Notification.objects.all().values()
        notycount = noty.count()
        request.session["noty"]=notycount
       
        return HttpResponseRedirect("/addnotifications")
    template =loader.get_template("dashboard/addnotifications.html")
    return HttpResponse(template.render({},request))







