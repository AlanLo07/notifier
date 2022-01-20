import time 
import requests
from NotifyWin10 import ToastNotifier
import webbrowser

if __name__ == '__main__':
    markets = []
    """ markets = [
        {
            'symbol': '^IXIC', 
            'price': 14340.255, 
            'change': -1.1487061, 
            'time': 1642630558, 
            'name': 'NASDAQ Composite'
        }, 
        {
            'symbol': '^N225', 
            'price': 27499.3, 
            'change': 0.11675844, 
            'time': 1642640205, 
            'name': 'Nikkei 225'
        }, 
        {
            'symbol': '^GDAXI', 
            'price': 15809.72, 
            'change': 0.23560004, 
            'time': 1642611299, 
            'name': 'DAX PERFORMANCE-INDEX'
        }
    ] """
    marketSummary = None
    toast = ToastNotifier()

    while True:
        try:
            marketSummary = requests.get(
                "https://yfapi.net/v6/finance/quote?symbols=%5EIXIC%2C%5EN225%2C%5EGDAXI",
                headers={"X-API-KEY":"iawz6uSnhral60DNR3rsE7KqkyVf0xqG31cuJcT3"}
                )
        except:
            #if the data is not fetched due to lack of internet
            print("Please! Check your internet connection")
        if not markets:

            if (marketSummary != None):
                #converting data into JSON format
                data = marketSummary.json()["quoteResponse"]["result"]
                
                #getting the data from the JSON
                for market in data:
                    market = {
                        "symbol": market["symbol"],
                        "price": market["regularMarketPrice"],
                        "change": market["regularMarketChangePercent"],
                        "time": market["regularMarketTime"],
                        "name": market["shortName"],
                    }

                    markets.append(market)
                del data
        else:
            if True:
                #converting data into JSON format
                data = marketSummary.json()["quoteResponse"]["result"]
                message = ""
                for i,market in enumerate(markets):
                    if market["time"] != data[i]["regularMarketTime"]:
                        market["price"] = data[i]["regularMarketPrice"]
                        market["change"] = data[i]["regularMarketChangePercent"]
                        market["time"] = data[i]["regularMarketTime"]
                        if market["change"] > 0.5:
                            message += "The price of {} has increased by {} percent.\n".format(market["name"], market["change"])
                        elif market["change"] < -0.5:
                            message += "The price of {} has decreased by {} percent.\n".format(market["name"], market["change"])
                if message:
                    toast.show_toast(
                       title="Market Update", 
                       msg=message,
                       icon_path="info.ico",
                       callback_on_click=lambda: webbrowser.open("https://smartrader.io/"),
                    )
                    del data

            time.sleep(24*60*60 / 100)