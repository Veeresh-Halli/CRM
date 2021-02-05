from django.http import HttpResponse

from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.auth.models import Group

from .decorators import unauthenticated_User,admin_Only

from django.contrib import messages

from .models import *

from .form import OrderForm
from .form import CreationForm


from django.core.cache import cache
# Create your views here.

@login_required(login_url='login')
@admin_Only
def index(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers,'toatle_customers':total_customers,'orders':orders,'total_orders': total_orders,'delivered': delivered, 'pending': pending}
    return render(request, 'index.html',context)

@login_required(login_url='login')
@admin_Only
def customers(request,customerId):
    customers = Customer.objects.get(id=customerId)
   
    customer_orders = customers.order_set.all()

    total_count = customer_orders.count()

    context = {'customers': customers,'customer_orders':customer_orders,'total_count':total_count}
    return render(request, 'customers.html',context)

@login_required(login_url='login')
def CreateOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    

    form = OrderForm(initial={'customer':customer})

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form,'customer':customer}
    return render(request,'create_order.html',context)

@login_required(login_url='login')
def UpdateOrder(request, pk):
    
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={'form':form}
    return render(request,'create_order.html',context)

@login_required(login_url='login')
def DeleteOrder(request,dk):
    order = Order.objects.get(id=dk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context={'order':order}
    return render(request,'delete_order.html',context)

@unauthenticated_User
def RegisterPage(request):
   
    form = CreationForm()

    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.info(request,"Account was suuccessfully created for " +username)
            return redirect('login')

    context = {'form':form}
    return render(request,'register.html',context)

@unauthenticated_User
def LoginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.info(request,"Username or Password is incorrect...")
    context={}
    return render(request,'login.html',context)


def LogoutPage(request):
    logout(request)
    request.session.flush()
    return redirect('login')
  

@login_required(login_url='login')
def UserPage(request):
    
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    ip = request.session.get('ip',0)
    user = request.user
    ct = cache.get('count', version=user.pk)
    context = {'orders':orders,'total_orders':total_orders, 'ip':ip, 'ct':ct}
    return render(request, 'user.html',context)

@login_required(login_url='login')
@admin_Only
def AdminRegisterPage(request):
   
    form = CreationForm()

    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff=True
            user.save()
        
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='admins')
            user.groups.add(group)

            messages.info(request,"Account was suuccessfully created for  " +username)
            

    context = {'form':form}
    return render(request,'adminRegister.html',context)


def Admin(request):
    return HttpResponse("You are not authorized to view this")


def Cust_CreateOrder(request,pk):
    user = User.objects.get(id=pk)

    form = OrderForm()

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form,'user':user}

    return render(request,'cust_create_order.html',context)