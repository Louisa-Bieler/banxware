import pandas as pd
import requests
import json

trans_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
auth = {'Authorization':'34044a757e0385e54e8c5141bad3bb3abb463727afac3cccb8e31d313db9a370'}
balance_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
verify_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/verify'

def make_transaction_df(api_url, auth):
    """Returns a df from the transactions api call at runtime"""
    data = requests.get(api_url, headers=auth)
    df = pd.read_json(data.text)
    new_df = pd.DataFrame.from_records(df['transactions'])
    return new_df

def make_balance_df(api_url, auth):
    """Returns a df from the balance api call at runtime"""
    response = requests.get(api_url, headers=auth)
    balance = json.loads(response.text)
    df = pd.DataFrame(balance, index=[0])
    return df

def with_cancelled_transaction_total(transactions, balance):
    """Returns including cancelled transactions df grouped by date"""
    transactions_dated = transactions.astype({'date': 'datetime64[ns]'})
    transactions_dated['dates'] = pd.to_datetime(transactions_dated['date']).dt.date
    transactions_grouped =  pd.DataFrame(transactions_dated.groupby(['dates']).sum().sort_values(by='dates', ascending=False))    
    balance = int(balance['amount'].values)

    new_array = []

    for record in transactions_grouped['amount'].values:
        new_record = balance - record
        new_array.append(new_record)
        balance = new_record
    
    transactions_grouped["running_total"] = new_array

    return transactions_grouped


def transform_transactions_by__not_status(transactions, balance):
    """Returns non-cancelled transactions df grouped by date"""
    transactions_dated = transactions.astype({'date': 'datetime64[ns]'})
    transactions_dated['dates'] = pd.to_datetime(transactions_dated['date']).dt.date
    transactions_dated_status = pd.DataFrame(transactions_dated[transactions_dated['status'] != 'CANCELLED'])
    transactions_grouped =  pd.DataFrame(transactions_dated_status.groupby(['dates']).sum().sort_values(by='dates', ascending=False))    
    balance = int(balance['amount'].values)

    new_array = []

    for record in transactions_grouped['amount'].values:
        new_record = balance - record
        new_array.append(new_record)
        balance = new_record
    
    transactions_grouped["running_total"] = new_array

    return transactions_grouped

def make_processed_df(df, balance):
    """Returns non-cancelled transactions df grouped by date"""
    transactions_dated = df.astype({'date': 'datetime64[ns]'})
    transactions_dated['dates'] = pd.to_datetime(transactions_dated['date']).dt.date
    transactions_dated_status = pd.DataFrame(transactions_dated[transactions_dated['status'] == 'PROCESSED'])
    transactions_grouped =  pd.DataFrame(transactions_dated_status.groupby(['dates']).sum().sort_values(by='dates', ascending=False))    
    balance = int(balance['amount'].values)

    new_array = []

    for record in transactions_grouped['amount'].values:
        new_record = balance - record
        new_array.append(new_record)
        balance = new_record
    
    transactions_grouped["running_total"] = new_array

    return transactions_grouped

def make_test_df(api_url, auth):
    """Returns a df from the verification api call at runtime"""
    data = requests.get(api_url, headers=auth)
    df = pd.read_json(data.text)
    new_df = pd.DataFrame.from_records(df['runningBalances'])
    return new_df