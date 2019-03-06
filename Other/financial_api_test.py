import requests
import pandas as pd

api_key = "PQyGMdEdKnn5JJKJEjROp3Wij9yjgEmC"

tickers = ["AAPL","NVDA","WMT"]

sim_ids = []
for ticker in tickers:

    request_url = f'https://simfin.com/api/v1/info/find-id/ticker/{ticker}?api-key={api_key}'
    content = requests.get(request_url)
    data = content.json()

    if "error" in data or len(data) < 1:
        sim_ids.append(None)
    else:
        sim_ids.append(data[0]['simId'])

print(sim_ids)

# define time periods for financial statement data
statement_type = "pl"
time_periods = ["Q1","Q2","Q3","Q4"]
year_start = 2013
year_end = 2018

writer = pd.ExcelWriter("simfin_data.xlsx", engine='xlsxwriter')

data = {}
for idx, sim_id in enumerate(sim_ids):
    d = data[tickers[idx]] = {"Line Item": []}
    if sim_id is not None:
        for year in range(year_start, year_end + 1):
            for time_period in time_periods:

                period_identifier = time_period + "-" + str(year)

                if period_identifier not in d:
                    d[period_identifier] = []

                request_url = f'https://simfin.com/api/v1/companies/id/{sim_id}/statements/standardised?stype={statement_type}&fyear={year}&ptype={time_period}&api-key={api_key}'

                content = requests.get(request_url)
                statement_data = content.json()

                # collect line item names once, they are the same for all companies with the standardised data
                if len(d['Line Item']) == 0:
                    d['Line Item'] = [x['standardisedName'] for x in statement_data['values']]

                if 'values' in statement_data:
                    for item in statement_data['values']:
                        d[period_identifier].append(item['valueChosen'])
                else:
                    # no data found for time period
                    d[period_identifier] = [None for _ in d['Line Item']]

df = pd.DataFrame(data=d)
print(df)