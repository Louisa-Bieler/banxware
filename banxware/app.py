from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import ast
import datetime as dt



app = Dash(__name__)

trans_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
auth = {'Authorization':'34044a757e0385e54e8c5141bad3bb3abb463727afac3cccb8e31d313db9a370'}
balance_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
def make_transaction_df(api_url, auth):
    data = requests.get(api_url, headers=auth)
    df = pd.read_json(data.text)
    new_df = pd.DataFrame.from_records(df['transactions'])
    return new_df

def make_balance_df(api_url, auth):
    response = requests.get(balance_url, headers=auth)
    balance = ast.literal_eval(response.text)
    df = pd.DataFrame(balance, index=[0])
    return df

def transform_transactions(transactions):
    transactions_dated = transactions.astype({'date': 'datetime64[ns]'})
    transactions_dated['dates'] = pd.to_datetime(transactions_dated['date']).dt.date
    transactions_grouped = transactions_dated.groupby(['dates']).sum()
    return transactions_grouped


transactions = make_transaction_df(trans_url, auth=auth)
balance = make_balance_df(balance_url, auth)


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

#app.layout = html.Div(children=[
 #   html.H1(children='Hello Dash'),

  #  html.Div(children='''
   #     Dash: A web application framework for your data.
    #'''),

  #  dcc.Graph(
   #     id='example-graph',
    #    figure=fig
   # )
#])

if __name__ == '__main__':
    app.run_server(debug=True)