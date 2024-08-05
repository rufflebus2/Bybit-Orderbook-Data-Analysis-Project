import pandas as pd
import json
import csv
import testing_bybit

def stats(df,symbol):
    # Statistics for Orderbook Update Latency
    mean = df.mean()
    median = df.median()
    min = df.min()
    max = df.max()
    with open('orderbook_statistics.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([symbol,mean,median,min,max])

def analysis():
    # Make sure tickers.json exists
    with open('tickers.json') as f: 
        symbols = json.load(f)

    # Create the clean orderbook_statistics file
    with open('orderbook_statistics.csv','w',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(['Ticker','Mean (ms)','Median (ms)','Min (ms)','Max (ms)'])
    
    df = pd.read_csv('orderbook_updates_task.csv', header=None)
    for symbol in symbols:
        logUpdateTime = df.loc[df[1]==symbol][2] # Timestamps of log update for selected ticker symbol
        snapshotTimeStamp = df.loc[df[1]==symbol][3] # Timestamp of orderbook snapshot for selected ticker symbol
        latency_df = logUpdateTime - snapshotTimeStamp # Latency of orderbook updating for selected ticker symbol
        stats(latency_df,symbol)

if __name__ == '__main__':
    testing_bybit.run_application()
    analysis()