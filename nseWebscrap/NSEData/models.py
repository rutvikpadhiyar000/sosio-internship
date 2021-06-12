from django.db import models

# Create your models here.

# Saves Information about CALLS and PUTS fields of table
class mainData(models.Model):
    strikePrice = models.IntegerField()
    expiryDate = models.TextField(max_length=15)
    underlying = models.TextField(max_length=15)
    identifier = models.TextField(max_length=50)
    openInterest = models.IntegerField()
    changeinOpenInterest = models.IntegerField()
    pchangeinOpenInterest = models.FloatField()
    totalTradedVolume = models.IntegerField()
    impliedVolatility = models.FloatField()
    lastPrice = models.FloatField()
    change = models.FloatField()
    pChange = models.FloatField()
    totalBuyQuantity = models.IntegerField()
    totalSellQuantity = models.IntegerField()
    bidQty = models.IntegerField()
    bidprice = models.FloatField()
    askQty = models.IntegerField()
    askPrice = models.FloatField()
    underlyingValue = models.FloatField()

# Saves information of one complete row in table
class NSEInfo(models.Model):
    strikePrice = models.IntegerField()
    expiryDate = models.TextField(max_length=10)
    CE = models.ForeignKey(mainData, on_delete=models.CASCADE, related_name='+')
    PE = models.ForeignKey(mainData, on_delete=models.CASCADE, related_name='+')

# Saves information of one fetch of table
class NSEInfoGrouped(models.Model):
    datetime_created = models.DateTimeField()

    NSEInfo_start = models.IntegerField()
    NSEInfo_end = models.IntegerField()

# Saves all subscribers
class mailList(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)