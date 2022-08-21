import pandas as pd
import requests
from app import booked_processed, transactions_including_cancelled, processed_df, transactions
from funkies import make_test_df

trans_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/transactions'
auth = {'Authorization':'34044a757e0385e54e8c5141bad3bb3abb463727afac3cccb8e31d313db9a370'}
balance_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/balances'
verify_url = 'https://uh4goxppjc7stkg24d6fdma4t40wxtly.lambda-url.eu-central-1.on.aws/verify'

# make the dataframe for the test data
test_df = make_test_df(verify_url, auth)
# get the dates into the correct dtype as far as possible
test_df['dates'] = pd.to_datetime(test_df['timestamp'], dayfirst=True, errors='coerce')
# get rid of those rows whose values could not be "coerced" into datetime format
test_df.dropna(inplace=True)
# sort it by date
test_df.sort_values(by=['dates'], ascending=False)
test_df.set_index('dates', inplace=True)
print(test_df)
# do an "inner join" to find matching dates in test and target
result = pd.merge(test_df, booked_processed, left_index=True, right_index=True)

print(result)





