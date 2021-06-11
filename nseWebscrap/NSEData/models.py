from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class mainData(models.Model):
    strikePrice = models.IntegerField()
    expiryDate = models.TextField(max_length=10)
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

class CE(mainData):
    pass

class PE(mainData):
    pass
 
class NSEInfo(models.Model):
    strikePrice = models.IntegerField()
    expiryDate = models.TextField(max_length=10)
    CE = models.ForeignKey(CE, on_delete=models.CASCADE, related_name='+')
    PE = models.ForeignKey(PE, on_delete=models.CASCADE, related_name='+')

