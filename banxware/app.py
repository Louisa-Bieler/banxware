from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import ast
import datetime as dt

app = Dash(__name__)

#opening variables to run the api calls
trans_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
auth = {'Authorization':'34044a757e0385e54e8c5141bad3bb3abb463727afac3cccb8e31d313db9a370'}
balance_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# this function creates a pandas dataframe out of the results of the api call at runtime: 
# this will aid in sorting and grouping the data, as well as giving us a good input for our plot.ly graphics
def make_transaction_df(api_url, auth):
    """Returns a df from the transactions api call at runtime"""
    data = requests.get(api_url, headers=auth)
    df = pd.read_json(data.text)
    new_df = pd.DataFrame.from_records(df['transactions'])
    return new_df

# this function 
def make_balance_df(api_url, auth):
    """Returns a df from the balance api call at runtime"""
    response = requests.get(balance_url, headers=auth)
    balance = ast.literal_eval(response.text)
    df = pd.DataFrame(balance, index=[0])
    return df

def transform_transactions(transactions, balance):
    """Returns non-cancelled transactions df grouped by date"""
    transactions_dated = transactions.astype({'date': 'datetime64[ns]'})
    transactions_dated['dates'] = pd.to_datetime(transactions_dated['date']).dt.date
    transactions_dated_not_cancelled = pd.DataFrame(transactions_dated[transactions_dated['status'] != 'CANCELLED'])
    transactions_grouped =  pd.DataFrame(transactions_dated_not_cancelled.groupby(['dates']).sum().sort_values(by='dates', ascending=False))    
    balance = int(balance['amount'].values)

    new_array = []

    for record in transactions_grouped['amount'].values:
        new_record = balance - record
        new_array.append(new_record)
        balance = new_record
    
    transactions_grouped['running_total'] = new_array

    return transactions_grouped
   

transactions = make_transaction_df(trans_url, auth=auth)
balance = make_balance_df(balance_url, auth)
transactions_grouped = transform_transactions(transactions, balance)

print(transactions_grouped.head())

fig = px.line(transactions_grouped, x=transactions_grouped.index.values, y="running_total", hover_data=["amount"], labels={
                     "running_total": "Running Total (EUR)",
                     "x": "Date"}
                 )

app.layout = html.Div(children=[
    html.H1(children='Merchant Foo'),

    html.Div(children='''
        6 months of cashflow records
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)