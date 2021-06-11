import requests

# Create your views here.

class NSEIndia:
        NSE_URL = 'https://www.nseindia.com/api/option-chain-indices?symbol='
        def __init__(self):
            self.headers = {'User-Agent': 'Mozilla/5.0'}
            self.session = requests.Session()
            self.session.get('http://nseindia.com', headers=self.headers).content
        
        def get_market_data(self, type_of_data):
            data = self.session.get(f'{self.NSE_URL}{type_of_data}',
                                headers=self.headers).json()['filtered']['data']
                        
            return data

def home():
    context = {}
    nse = NSEIndia()
    data = nse.get_market_data('NIFTY')
    print(data[0]['CE'])
    # context['CE'] = data['CE']
    # context['PE'] = data['PE']
    # return render('index.html', context)

home()