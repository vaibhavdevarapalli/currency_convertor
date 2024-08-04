from requests import get
from pprint import PrettyPrinter
import os

BASE_URL = "https://free.currconv.com/"
API_KEY = "bfcfd3aa7dd4b3e217b8"  # Use environment variable if set

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        response = get(url)
        response.raise_for_status()
        data = response.json()
        if 'results' not in data:
            print("Error: 'results' key not found in the response.")
            return []
        data = list(data['results'].items())
        data.sort()
        return data
    except Exception as e:
        print(f"Error fetching currencies: {e}")
        return []

def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        response = get(url)
        response.raise_for_status()
        data = response.json()
        if not data:
            print('Invalid currencies.')
            return None
        rate = list(data.values())[0]
        print(f"{currency1} -> {currency2} = {rate}")
        return rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return
    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount

def main():
    currencies = get_currencies()
    if not currencies:
        print("Unable to fetch currencies. Exiting...")
        return

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()
        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")

if __name__ == "__main__":
    main()
