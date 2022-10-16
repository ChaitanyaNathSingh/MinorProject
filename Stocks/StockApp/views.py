
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, UserUpdateForm
from .models import Profile, UserStocks
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Stock, StockData
from django.db.models import Sum, Avg, Max, Min, Count

# Create your views here.

def home(request):
    return render(request, 'home.html')

def userhome(request):
    return render(request, 'userhome.html')

def adminhome(request):
    return render(request, 'adminhome.html')

def stocks(request):
    s = Stock.objects.all()
    return render(request, 'stock.html', {'stocks': s})

def addStock(request):
    if request.method == 'POST':
        Stock_name = request.POST['Stock_name']
        Stock_type = request.POST['Stock_type']
        Company_name = request.POST['Company_name']
        Stock_about = request.POST['Stock_about']
        Stock.objects.create(Stock_name=Stock_name, Stock_type=Stock_type, Company_name=Company_name,Stock_about=Stock_about)
        return redirect('/stocks')
    else:
        s = Stock.objects.all()
        return render(request, 'stock.html', {'stocks': s})

def deleteStock(request, pk):
    s = Stock.objects.get(Stock_id=pk)
    s.delete()
    return redirect('/stocks')

def stockData(request, pk):
    st = Stock.objects.get(Stock_id=pk)
    s = StockData.objects.filter(Stock_id=st)
    return render(request, 'stockData.html', {'stocks': s, 'st': st})  
    
def addStockData(request, pk):
    if request.method == 'POST':
        st = Stock.objects.get(Stock_id=pk)
        Stock_price = request.POST['Stock_price']
        Stock_date = request.POST['Stock_date']
        StockData.objects.create(Stock_id=st, Stock_price=Stock_price, Stock_date=Stock_date)
        return redirect('/stockData/'+str(pk))
    else:
        return redirect('/stockData/'+str(pk))

def buyStocks(request):
    s = Stock.objects.all()
    for i in s:
        i.Stock_date = StockData.objects.filter(Stock_id=i).aggregate(Max('Stock_date'))['Stock_date__max']
        i.Stock_price = StockData.objects.get(Stock_id=i, Stock_date=i.Stock_date).Stock_price
    return render(request, 'buyStocks.html', {'stocks': s})

def viewStocksData(request, pk):
    st = Stock.objects.get(Stock_id=pk)
    s = StockData.objects.filter(Stock_id=st)
    return render(request, 'viewStockData.html', {'stocks': s, 'st': st})  

def userStocks(request):
    u = User.objects.get(username=request.user.username)
    us = UserStocks.objects.filter(user=u)
    for i in us:
        i.Stock_date = StockData.objects.filter(Stock_id=i.Stock_id).aggregate(Max('Stock_date'))['Stock_date__max']
        i.price = StockData.objects.filter(Stock_id=i.Stock_id, Stock_date=i.Stock_date)[0].Stock_price
    return render(request, 'userStocks.html', {'stocks': us})

def buy(request, pk):
    u = User.objects.get(username=request.user.username)
    s = Stock.objects.get(Stock_id=pk)
    new = StockData.objects.filter(Stock_id=s).aggregate(Max('Stock_date'))['Stock_date__max']
    sp =StockData.objects.filter(Stock_id=new, Stock_date=new)[0].Stock_price
    sd = datetime.now()
    UserStocks.objects.create(user=u, Stock_id=s, Stock_price=sp, Stock_date=sd)
    return redirect('/userStocks')

def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        storage = messages.get_messages(request)
        storage.used = True
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            u = User.objects.get(username=username)
            if u.is_superuser:
                login(request, user)
                return redirect('/adminhome')
            if user is not None:
                login(request, user)
                return redirect('/userhome')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    system_messages = messages.get_messages(request)
    for message in system_messages:
        pass
    return render(request=request, template_name="userlogin.html", context={"login_form": form})

def userregister(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                        password=request.POST['password1'], first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'])
        Profile.objects.create(user=user,phone=request.POST['phone'],
                                gender=request.POST['gender'], location=request.POST['location'],
                                dob=request.POST['dob'])
        login(request, user)
        return HttpResponseRedirect('/userhome')
    else:
        form = RegistrationForm()
        userprofile = ProfileForm()
        return render(request=request, template_name="userregister.html",
                    context={"register_form": form, 'userprofileform': userprofile})

def user_details(request):
    if not request.user.is_superuser:
        return redirect('/')
    u = User.objects.filter(is_superuser=False)
    lp = []
    for i in u:
        j = Profile.objects.filter(user=i)
        if len(j) == 0:
            lu = [i.username, i.first_name + " " + i.last_name, i.email, " ", " ", " ", " ", " "]
            lp.append(lu)
        else:
            for p in j:
                lu = [i.username, i.first_name + " " + i.last_name, i.email, p.phone, p.gender,
                      p.dob, p.location]
                lp.append(lu)
    return render(request, 'user_details.html', {'data': lp})

def profile(request):
    u = request.user
    p = Profile.objects.get(user=u)
    return render(request, 'profile.html')

def updateprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'username': request.user.username,
        'email': request.user.email
    }
    return render(request, 'updateprofile.html', context)

def logout_req(request):
    logout(request)
    return HttpResponseRedirect('/')

def delete(request, pk):
    u = User.objects.get(username=pk)
    u.delete()
    return redirect('/user_details')
