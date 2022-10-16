from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER = ( ('Male','MALE') , ('Female','FEMALE') )  

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default=999999999)
    gender = models.CharField(choices=GENDER, default='MALE', max_length=6)
    dob = models.DateField()
    location = models.CharField(max_length=100,blank=False)

class Stock(models.Model):
    Stock_id = models.AutoField(primary_key=True)
    Stock_name = models.CharField(max_length=100, blank=False, unique=True)
    Stock_type = models.CharField(max_length=100, blank=False)
    Stock_about = models.CharField(max_length=1000, blank=False)    
    Company_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.Stock_name
    
    class Meta:
        ordering = ['Stock_id']
        verbose_name_plural = 'Stocks'

class StockData(models.Model):
    id = models.AutoField(primary_key=True)
    Stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Stock_price = models.FloatField()
    Stock_date = models.DateField()

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'StockData'

class UserStocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Stock_date = models.DateField(blank=True, null=True)
    Stock_price = models.FloatField()

    class Meta:
        ordering = ['user']
        verbose_name_plural = 'UserStocks'