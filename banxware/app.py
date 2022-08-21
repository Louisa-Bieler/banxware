from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import json
from funkies import make_transaction_df, make_balance_df,\
    transform_transactions_by__not_status, with_cancelled_transaction_total,\
        make_test_df, make_processed_df

# using Dash to do the heavy lifting
app = Dash(__name__)

# opening variables to run the api calls
trans_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
auth = {'Authorization':'34044a757e0385e54e8c5141bad3bb3abb463727afac3cccb8e31d313db9a370'}
balance_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
verify_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/verify'

# use the custom functions in "funkies" to create the data for plotting
transactions = make_transaction_df(trans_url, auth=auth)
balance = make_balance_df(balance_url, auth)
booked_processed = transform_transactions_by__not_status(transactions, balance)
transactions_including_cancelled = with_cancelled_transaction_total(transactions, balance)
test_df = make_test_df(verify_url, auth)
processed_df = make_processed_df(transactions, balance)

# making the plot.ly figures to put on the website
fig = px.line(booked_processed, x=booked_processed.index.values, y='running_total',
                hover_data=["amount"], labels={
                     "running_total": "Running Total (EUR)",
                     "x": "Date"}
                     )

fig1 = px.line(transactions_including_cancelled, x=transactions_including_cancelled.index.values, range_y=(2000, 22000), y="running_total", 
            hover_data=["amount"],  labels={
                     "running_total": "Running Total Including Cancelled (EUR)",
                     "x": "Date"}
                     )

fig2 = px.line(test_df, x=test_df.index, range_y=(2000, 22000), y="runningBalance", 
              labels={
                     "runningBalance": "Test Balance (EUR)",
                     "x": "Date"}
                     )

fig3 = px.line(processed_df, x=processed_df.index, range_y=(2000, 22000), y="running_total", 
              labels={
                     "running_total": "Processed Balance (EUR)",
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
    ),

    dcc.Graph(
        id='example-graph1',
        figure=fig1
    ),

    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),

    dcc.Graph(
        id='example-graph3',
        figure=fig3
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)