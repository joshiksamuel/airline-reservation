from django.shortcuts import render, redirect
from flight.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='signin')
def findflight(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        flight_list = Flight.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if flight_list:
            return render(request, 'flightlist.html', locals())
        else:
            context["error"] = "Sorry no flight availiable"
            return render(request, 'findflight.html', context)
    else:
        return render(request, 'findflight.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        name = request.POST['name']
        bankname = request.POST['bankname']
        accountno = request.POST['accountno']
        cardname = request.POST['cardname']
        cardno=request.POST['cardno']
        expyear=request.POST['expyear']
        obj=Payment()
        obj.name=name
        obj.bankname= bankname
        obj.accountno= accountno
        obj.cardname = cardname
        obj.cardno = cardno
        obj.expyear = expyear
        obj.save()
        id_r = request.POST.get('flight_id')
        seats_r = int(request.POST.get('no_seats'))
        flight = Flight.objects.get(id=id_r)
        if flight:
            if flight.rem > int(seats_r):
                name_r = flight.flight_name
                cost = int(seats_r) * flight.price
                source_r = flight.source
                dest_r = flight.dest
                nos_r = Decimal(flight.nos)
                price_r = flight.price
                date_r = flight.date
                time_r = flight.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = flight.rem - seats_r
                Flight.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, flight_name=name_r,
                                           source=source_r, flightid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'flightbookings.html', locals())
            
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'findflight.html', context)

    else:
        return render(request, 'findflight.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('flight_id')
        try:
            book = Book.objects.get(id=id_r)
            flight = Flight.objects.get(id=book.flightid)
            rem_r = flight.rem + book.nos
            Flight.objects.filter(id=book.flightid).update(rem=rem_r)
          
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that flight"
            return render(request, 'flighterror.html', context)
    else:
        return render(request, 'findflight.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'yourbookings.html', locals())
    else:
        context["error"] = "Sorry no flight booked"
        return render(request, 'findflight.html', context)



def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        user.save()
        if user:
            login(request, user)
            return redirect("signin")
        else:
            context["error"] = "Provide valid details"
            return render(request, 'sigin.html', context)
    else:
        return render(request, 'sigin.html', context) 
 
def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
           
            context["user"] = name_r
            context["id"] = request.user.id
            return redirect("home")
          
        else:
            context["error"] = "Username or password incorrect"
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'login.html', context)
@login_required(login_url='signin')
def contact(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        obj=Contact()
        obj.name = name
        obj.email = email
        obj.message = message
        obj.save()
        messages.success(request,"Register successfully")
    return render(request,'contact.html')



