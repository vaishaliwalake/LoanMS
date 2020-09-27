from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
from .models import Login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from users.ConnpoolUser import GetConn, db3
from selfserv.forms import CustomerForm,  SignUpForm

conn=GetConn()
db3curr=db3.cursor()


def LoadLoginPage(request):
      print("inside login load page function")
      template = loader.get_template ('login.html')
      return render (request, 'login.html')

def ValidateLogin(request):

    if request.method== 'POST' or request.method=='GET':

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            post = Login.objects.filter (username=username)
            if post:
                username = request.POST['username']
                posts =request.session['username'] = username
                query = Login.objects.filter (username=posts)

                return render (request, 'profile.html', {"query":query})
            else:
                return render (request, 'login.html', {})
        return render (request, 'login.html', {})

def profile(request):
        print('inside profile')
        if request.session.has_key ('username'):
            posts = request.session['username']
            query = Login.objects.filter (username=posts)
            return render (request, 'selfserv/profile.html', {"query":query})
        else:
             return render (request, 'login.html', {})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render (request, 'login.html', {})
    #return render (request, 'Customerform.html')

def CustomersApp(request):
    template = loader.get_template ('selfserv.html')

    context = {'home': 'selfserv/CustomersApp'}

    return HttpResponse (template.render (context, request))


def CustSelfserve(request):

    cust_id = request.GET['cust_id']

    print ("inside function", cust_id)

    db3curr.execute("select id, first_name,last_name, email from selfserv_login where id="+cust_id)
    loginDetail = db3curr.fetchone()
    template = loader.get_template('Customerform.html')
    form = CustomerForm (loginDetail)


    for n in form.data:
        print(n)

    context = {'home':'selfserv/CustSelfserve'}



    context = {'form': form, 'c_data':loginDetail}

    from django.shortcuts import render
    return HttpResponse(template.render(context, request))


def CustSaveData(request):
    if request.method== 'POST' or request.method=='GET':

     print("inside function")
     custForm=CustomerForm(request.POST)
     if custForm.is_valid ():
         print ("valid")
         custForm.save(commit=True)

         return render (request, 'Customerform.html')



def CheckStatus(request):
    cust_id=request.GET['cust_id']
    print('customer id to check status -->', cust_id)
    db3curr.execute ("select c.cust_id, c.first_name,c.last_name,c.email,c.CreditScore, c.RequestedLoanAmount, c.DurationInMonths,cl.application_status as Status from selfserv_customers c left join cust_loans cl on cl.cust_id=c.cust_id where c.cust_id="+cust_id)
# use fetchall() to get the list of row data
    l_data = []

    for cust_id,first_name,last_name,email,CreditScore, RequestedLoanAmount, DurationInMonths,Status in db3curr.fetchall ():
     l_data.append ({"id":cust_id,
                    "first_name":first_name,
                    "last_name":last_name,
                    "email":email
                       , "CreditScore": CreditScore

                       , "RequestedLoanAmount": RequestedLoanAmount
                       , "DurationInMonths": DurationInMonths
                     , "Status" : Status})


# Create Template Object
    template = loader.get_template ('status.html')
    context = { 'l_data': l_data}
    return HttpResponse (template.render (context, request))

def loadSignup(request):
    print('load signup')
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signupValidate(request):
    print('in sign up validation')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"login.html")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

