import json
import asyncio
from pybit.unified_trading import HTTP
import csv
import aiocsv
import aiofiles
import concurrent.futures
import time

def sort_ask(retrieved): # Ask side information is retrieved in ascending order, must reverse order 
    sorted_ask = sorted(retrieved, key=lambda x: float(x[0]), reverse=True)
    return sorted_ask

def check_updated(existing, retrieved): # Check if retrieved order book cache is updated or the same as previous cache
    return not (existing == retrieved)

class OrderBookCache:
    def __init__(self, ticker):
        self.ticker = ticker # Each OrderBookCache has a specific ticker symbol
        self.ts = None
        self.bid = None
        self.ask = None
    
    def log_update(self,update,side):
        update_time = time.time() * 1000 # Timestamp of log update is in milliseconds
        # async with aiofiles.open('orderbook_updates_task.csv', 'a') as file:
        with open('orderbook_updates_task.csv','a',newline='') as file: # Open orderbook update log and append updates
            # writer = aiocsv.AsyncWriter(file)
            writer = csv.writer(file)
            writer.writerow([side,self.ticker,update_time,self.ts,update])
    
    def update_book(self,bid,ask,ts):
        bid_update = check_updated(self.bid, bid)
        ask_update = check_updated(self.ask, ask)
        side = 'bid' if bid_update else None
        side = 'ask' if ask_update else side
        side = 'both' if bid_update and ask_update else side

        if bid_update or ask_update: # Check if bid/ask updated
            self.bid = bid
            self.ask = ask
            self.ts = ts
            self.log_update([bid,ask],side)
            # print(f'{self.ticker}\tBID\t{ts}')
            # print(f'{self.ticker}\tASK\t{ts}')

    def print_order_book(self): # Print first 5 levels of orderbook on each side
        print(f"Order Book for {self.ticker}:")
        for order in self.ask:
            print(f"(ASK) Price: {order[0]}\tSize: {order[1]}")
        print()
        for order in self.bid:
            print(f"(BID) Price: {order[0]}\tSize: {order[1]}")
        print()

class WebSocketListener:
    def __init__(self, ticker_symbols):
        self.session = HTTP()
        self.ticker_symbols = ticker_symbols
        self.caches = {}

    async def process_symbol(self, symbol):
        # start_time = time.time()
        # elapsed_time = 0
        # while elapsed_time < 60: # Listen for 60 seconds
            orderbook = self.session.get_orderbook(
                category='linear',
                symbol=symbol,
                limit='5'
            )
            # await asyncio.sleep(0) # Allows for asynchronous running
            bid = orderbook['result']['b'] # Bid information (5 levels)
            ask = sort_ask(orderbook['result']['a']) # Ask information (5 levels)
            ts = orderbook['result']['ts'] # Timestamp of orderbook snapshot

            if self.caches.get(symbol) is None: # If OrderBookCache for ticker symbol does not exist, make one
                self.caches[symbol] = OrderBookCache(symbol)
            
            self.caches.get(symbol).update_book(bid,ask,ts) # Update OrderBookCache
            # elapsed_time = time.time()-start_time

    async def main(self):
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 60: # Listen for 60 seconds
            start_new_loop = time.time()
            tasks = [self.process_symbol(symbol) for symbol in self.ticker_symbols]
            await asyncio.gather(*tasks)
            elapsed_time = time.time()-start_time
            print(time.time()-start_new_loop)

def run_application():
    # Make sure tickers.json exists
    with open('tickers.json') as f: 
        symbols = json.load(f)

    # Create the clean orderbook_update file
    with open('orderbook_updates_task.csv','w',newline='') as file:
        writer = csv.writer(file)
    
    listener = WebSocketListener(symbols)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listener.main())