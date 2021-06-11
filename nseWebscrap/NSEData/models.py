from django.db import models

# Create your models here.

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
 
class NSEInfo(models.Model):
    strikePrice = models.IntegerField()
    expiryDate = models.TextField(max_length=10)
    CE = models.ForeignKey(mainData, on_delete=models.CASCADE, related_name='+')
    PE = models.ForeignKey(mainData, on_delete=models.CASCADE, related_name='+')

