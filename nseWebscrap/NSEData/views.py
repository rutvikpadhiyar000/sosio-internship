from django.shortcuts import render
import requests
from .models import mainData, NSEInfo

# Create your views here.

def commit_data(all_data):
    NSEInfo.objects.all().delete()
    mainData.objects.all().delete()
    for data in all_data:
        ce = mainData.objects.create(**(data['CE']))
        pe = mainData.objects.create(**(data['PE']))
        full_row = NSEInfo.objects.create(
            strikePrice = data['strikePrice'],
            expiryDate = data['expiryDate'],
            CE = ce,
            PE = pe
        )

def get_market_data(type_of_data = None):
    if type_of_data is None:
        type_of_data = "NIFTY"
    NSE_URL = 'https://www.nseindia.com/api/option-chain-indices?symbol='
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()
    data = session.get(f'{NSE_URL}{type_of_data}',
                headers=headers).json()['filtered']['data']
                        
    return data

def home(request):
    context = {}
    all_data = get_market_data('NIFTY')
    commit_data(all_data)
    context['data'] = all_data
    return render(request, 'index.html', context)