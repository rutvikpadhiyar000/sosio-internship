from django.shortcuts import render
import requests
from .models import mainData, NSEInfo, NSEInfoGrouped
from django.utils import timezone
import time
import threading

# Create your views here.

# This keeps track of visitors.
total_home_page_load = 0 


def get_rows_from_rowGroup(row_group_data):
    row_list = []
    for i in range(row_group_data.NSEInfo_start, row_group_data.NSEInfo_end+1):
        row_list.append(NSEInfo.objects.get(id=i))
    return row_list


def home(request):
    global total_home_page_load

    if not total_home_page_load:
        th = threading.Thread(target=refresh_database)
        th.start()
        # if database is empty it may give error so we wait till refresh_database
        # finishes executing (only happens for first request)
        time.sleep(15)

    total_home_page_load+=1

    # uses database objects so may give error for empty database.
    context = {}
    row_group_data = NSEInfoGrouped.objects.order_by('id')[0]
    all_data = get_rows_from_rowGroup(row_group_data)
    context['data'] = all_data
    return render(request, 'index.html', context)

# These runs on saparate thred and refresh database every 3 minuts.

def refresh_database():
    while True:
        try:
            get_market_data()
        except:
            # if there is error try after
            # some time (it gives error when 
            # api is updating) 
            time.sleep(3)
            refresh_database()
        time.sleep(180)

def get_market_data(type_of_data = None):
    if type_of_data is None:
        type_of_data = "NIFTY"
    NSE_URL = 'https://www.nseindia.com/api/option-chain-indices?symbol='
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()
    data = session.get(f'{NSE_URL}{type_of_data}',
                headers=headers).json()['filtered']['data']
                        
    commit_data(data)

def commit_data(all_data):
    print("REFRESHED")

    # Saves all rows added in NSEInfo table
    full_row_added = []

    # Iterate through all_data to get database rows
    for data in all_data:
        ce = mainData.objects.create(**(data['CE']))
        pe = mainData.objects.create(**(data['PE']))
        full_row = NSEInfo.objects.create(
            strikePrice = data['strikePrice'],
            expiryDate = data['expiryDate'],
            CE = ce,
            PE = pe
        )

        # Saving Start and end index of NSEInfo in NSEInfoGrouped so that 
        # it can be accessed easly.
        full_row_added.append(full_row.id)
    NSEInfoGrouped.objects.create(
        datetime_created = timezone.now(),
        NSEInfo_start = min(full_row_added),
        NSEInfo_end = max(full_row_added)
    )
