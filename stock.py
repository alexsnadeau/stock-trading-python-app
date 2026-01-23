import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()

#call API key from .env file
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def run_stock_job():

    url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit=100&sort=ticker&apiKey={POLYGON_API_KEY}'

    response = requests.get(url)
    tickers = []

    # could do print(data.keys) to get the keys and figure out how to get the tickers

    data = response.json()
    for ticker in data['results']:
        tickers.append(ticker)

    count = 0

    while 'next_url' in data and count < 5:
        next_url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
        response = requests.get(next_url)
        data = response.json()

        results = data.get('results')

        if results:
            for ticker in data['results']:
                tickers.append(ticker)
            count += 1 #Increment after a success
        else:
            break

# can use this code but polygon has a limit so it won't run the full code. must add a limit to the while statement
        
    example_ticker = {'ticker': 'AMR', 
                    'name': 'Alpha Metallurgical Resources, Inc.', 
                    'market': 'stocks', 
                    'locale': 'us', 
                    'primary_exchange': 'XNYS', 
                    'type': 'CS', 
                    'active': True, 
                    'currency_name': 'usd', 
                    'cik': '0001704715', 
                    'composite_figi': 'BBG00DGWV035', 
                    'share_class_figi': 'BBG00DGWV044', 
                    'last_updated_utc': '2026-01-20T07:05:28.530088098Z'}

    fieldnames = list(example_ticker.keys())
    output_csv = 'tickers.csv'
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ticker in tickers:
            row = {key: ticker.get(key, '') for key in fieldnames}
            writer.writerow(row)

#this means if I call the script directly, it will still run the function, but if I import it, it won't run automatically unless I call it
if __name__ == "__main__":
    run_stock_job()