from django.db.models import Q
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from cstoreapp.models import product,cart,order
import random
import razorpay

# Create your views here.
def home(request):
    name=request.user.username
    context={}
    context['nme']=name
    p=product.objects.filter(availability=True)
    context['products']=p
    return render(request,'home.html',context)

def viewcart(request):
    if request.user.is_authenticated:
        c=cart.objects.filter(uid=request.user.id)
        sum=0
        for i in c:
            sum=sum+i.pid.Price*i.qty
        context={}
        if len(c)==0:
            context['errmsg']="Your cart is currently empty,click this dialogue to continue shopping."
        context['items']=len(c)
        context['total']=sum
        context['data']=c
        return render(request,'viewcart.html',context)
    else:
        context={}
        context['errmsg1']="You must be logged in to view your cart,click this dialogue to login."
        return render(request,'viewcart.html',context)


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        if n==1:
            context["errmsg"]="Product already exists in cart"
            return render(request,'productview.html',context)
        else:
            c=cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context["products"]=p
            context["success"]="Product is added to cart."
            return render(request,'productview.html',context)
    else:
        return redirect('/userlogin')
    
def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    for x in c:
        o=order.objects.create(orderid=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    np=len(orders)
    sum=0
    for i in orders:
        sum=sum+i.pid.Price*i.qty
    if len(orders)==0:
        context['errmsg2']="You need to add products to cart first and place order,there are no orders placed currently."
    context['items']=len(orders)
    context['total']=sum
    context['data']=orders
    return render(request,'placeorder.html',context)

def removeorder(request,pid):
    o=order.objects.filter(id=pid)
    o.delete()
    return redirect('/placeorder')

def payment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.Price*x.qty
        oid=x.orderid
    client = razorpay.Client(auth=("rzp_test_dHAbGySAHUx3mH", "Hz0nDRWxMNagkgBVKaSfhJD1"))
    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'payment.html',context)

def userlogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['pwd']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Username or password cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                context['sucessmsg']="Logged in sucessfully."
                return redirect('/home')
            else:
                context['errmsg']="Invalid Credentials"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        email=request.POST['email']
        upass=request.POST['pwd']
        cpass=request.POST['cpwd']
        context={}
        if uname=="" or email=="" or upass=="" or cpass=="":
            context['errmsg']="Fields cannot be empty!"
            return render(request,'register.html',context)
        elif upass!=cpass:
            context['errmsg']="Password is not matching!"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=email)
                u.set_password(upass)
                u.save()
                context['sucessmsg']="User has been created sucessfully try logging in now."
                return render(request,'register.html',context)
            except Exception:
                context['msg']="This user already exists.Try logging in!"
                return redirect('/login')
    else:
        return render(request,'register.html')
    
def userlogout(request):
    logout(request)
    return redirect('/home')

def productview(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'productview.html',context)

def myaccount(request):
    info = {
    'username': request.user.username,
    'email': request.user.email,
    }
    context={}
    context['uinfo']=info
    return render(request,'myaccount.html',context)

def byprice(request,prc):
    if prc=='0':
        col='Price'
    else:
        col='-Price'
    context={}
    p=product.objects.filter(availability=True).order_by(col)
    context['products']=p
    return render(request,'home.html',context)

def bycatagory(request,ctg):
    context={}
    c1=Q(availability=True)
    c2=Q(catagory=ctg)
    p=product.objects.filter(c1 & c2)
    context['products']=p
    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')
    

