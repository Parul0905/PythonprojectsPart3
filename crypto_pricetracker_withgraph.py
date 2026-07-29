import os
import csv
from datetime import datetime
import requests
import matplotlib.pyplot as plt

API_URL = "https://api.coingecko.com/api/v3/simple/price"
PARAMS = {
    'ids': 'bitcoin,ethereum,solana',
    'vs_currencies': 'usd'
}

CSV_FILE = 'crypto_prices.csv'

def fetch_crypto_data():
    response=requests.get(API_URL,params=PARAMS)
    return response.json()

def save_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'coin', 'price'])

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        for coin_id, coin_data in data.items():
            writer.writerow([timestamp, coin_id, coin_data.get('usd')])

    print("✅ DATA SAVED TO CSV ")

def plot_graph(coin_id):
    times = []
    prices = []

    with open(CSV_FILE, "r", newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 3:
                continue
            if row[1] == coin_id:
                times.append(datetime.strptime(row[0], "%Y-%m-%d %H-%M-%S"))
                prices.append(float(row[2]))

    if not times:
        print(f'No data found for {coin_id}')
        return

    plt.figure(figsize=(10,7))
    plt.plot(times, prices, marker='o')
    plt.title(f'{coin_id.capitalize()} Price History')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    print("Fetching live crypto data ....")
    crypto_data=fetch_crypto_data()
    save_to_csv(crypto_data)

    print("-" * 40)
    for coin_id, coin_data in crypto_data.items():
        print(f"{coin_id} - ${coin_data.get('usd')}")

    choice = input("Enter the coin name to get graph:").strip()
    if choice:
        plot_graph(choice)

if __name__=="__main__":
    main()
