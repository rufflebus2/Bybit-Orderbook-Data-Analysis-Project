# Bybit-Orderbook-Data-Analysis-Project
Version: Python 3.10.11

## Instructions
There are 3 required files to run the application.
1. testing_bybit.py 

This file is the class and function definitions file. These classes and functions will be used in the orderbook_analysis.py file.

2. orderbook_analysis.py 

This file is the main file to run the application.

3. tickers.json

This file is required for reading the ticker symbols to be read.

To run the application, we can use the command "python3 orderbook_analysis.py" in the terminal. The application will listen to the connected WebSocket server for 60 seconds. After that, 2 files will be generated.

1. orderbook_updates_task.py

This is the log of orderbook cache updates that have occurred in the 60 seconds of code running. This file will then be used for the statistics file.

2. orderbook_statistics.py 

This contains the statistics regarding latency of the orderbook cache updates. The latency is calculated by taking the timestamp of the retrieved orderbook snapshot and subtracting it from the timestamp of updating the local orderbook cache. This latency is measured in milliseconds (ms).
