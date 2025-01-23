from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=4)
    rem = models.DecimalField(decimal_places=0, max_digits=4)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.flight_name

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    flightid=models.DecimalField(decimal_places=0, max_digits=2)
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=4)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    
    def __str__(self):
        return self.name
    
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=20)
    message=models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Payment(models.Model):
    name=models.CharField(max_length=50)
    bankname=models.CharField(max_length=50)
    accountno=models.IntegerField(blank=True,null=True)
    cardname=models.CharField(max_length=50,blank=True,null=True)
    cardno=models.IntegerField(blank=True,null=True)
    expyear=models.DateField(blank=True,null=True)
    def __str__(self):
        return self.bankname