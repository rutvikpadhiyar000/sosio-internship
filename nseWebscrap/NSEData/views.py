from django.shortcuts import redirect, render
import requests
from .models import mainData, NSEInfo, NSEInfoGrouped, mailList
from django.utils import timezone
import time
import threading
from json.decoder import JSONDecodeError
from django.conf import  settings
from django.core.mail import send_mail

# Create your views here.

# This keeps track of visitors.
total_home_page_load = 0 

# True if there are no subscribers
no_subscriber = True

def get_rows_from_rowGroup(row_group_data):
    row_list = []
    for i in range(row_group_data.NSEInfo_start, row_group_data.NSEInfo_end+1):
        row_list.append(NSEInfo.objects.get(id=i))
    return row_list


def home(request):
    global total_home_page_load
    # runs refresh database on saparate thred every 3 mins.
    if total_home_page_load == 0:
        th = threading.Thread(target=refresh_database)
        th.start()

        # if database is empty it may give error so we wait till refresh_database
        # finishes executing (only happens for first request)
        time.sleep(15)


    # uses database objects so may give error for empty database.
    context = {}
    row_group_data = NSEInfoGrouped.objects.last()
    all_data = get_rows_from_rowGroup(row_group_data)
    context['data'] = all_data
    total_home_page_load+=1
    return render(request, 'index.html', context)


def subscribe(request):
    return render(request, 'subscribe.html')

def subscribe_to_mail_list(request):
    global subscriber_count

    name = request.POST['name']
    email = request.POST["email"]
    mailList.objects.create(
        name=name,
        email=email
    )

    if no_subscriber:
        thr = threading.Thread(target=send_mail_to_all)
        thr.start()

    welcome_mail(email=email, name=name)

    # Sends to home page when process is complete
    return redirect('/')

def welcome_mail(email=None, name=None):
    if name==None:
        name = 'User'
    subject = "Wellcome to nsewebscrap"
    message = f"Hello {name}, \n\n Your subscription was successfull"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = mailList.objects.all().values_list('email', flat=True)
    send_mail(subject, message, email_from, recipient_list )
    

"""These runs on saparate thred and refresh
    database every 3 minuts."""

def refresh_database():
    
    while True:
        try:
            # it gives error when api is updating
            get_market_data()
            time.sleep(180)
        except JSONDecodeError:
            # if there is error try after 3 seconds 
            time.sleep(3)

def get_market_data(type_of_data = "NIFTY"):
    NSE_URL = 'https://www.nseindia.com/api/option-chain-indices?symbol='
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()
    data = session.get(f'{NSE_URL}{type_of_data}',
                headers=headers).json()['filtered']['data']

    commit_data(data)

def commit_data(all_data):

    # Saves all rows added in NSEInfo table
    full_row_added = []
    # True if LPC (pChange) is grater than 10% for any row.
    sent_mail = False

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

"""This is mail sending function runs every 60 minuts
and sends mail to every on if any row has more than 
10% change in LTP"""

def send_mail_to_all():

    while True:
        if changed_more_than_ten_percent():
            subject = "More than 10% change in last hour."
            message = "you are getting this mail because you are subscribed."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = mailList.objects.all().values_list('email', flat=True)
            send_mail( subject, message, email_from, recipient_list )
        time.sleep(3600)

def changed_more_than_ten_percent():
    latest_data = NSEInfoGrouped.objects.last()
    try:
        data_before_1_hour = NSEInfoGrouped.objects.get(id=latest_data.id - 20)
    except:
        return False
    else:
        # convert data into list
        latest_data = get_rows_from_rowGroup(latest_data)
        data_before_1_hour = get_rows_from_rowGroup(data_before_1_hour)

        # check all prices for grater than 10% diffrence
        for i in range(min(latest_data, data_before_1_hour)):
            ten_percent_ce = (latest_data[i].ce).lastPrice // 10
            ten_percent_pe = (latest_data[i].pe).lastPrice // 10
            if (abs((latest_data[i].ce).lastPrice - (data_before_1_hour[i].ce).lastPrice)
                or abs((latest_data[i].pe).lastPrice - (data_before_1_hour[i].pe).lastPrice)):
                return True
        return False