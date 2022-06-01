import requests
import pandas as pd
from pandas import json_normalize


def get_exchange_rates(data):
    base_url = 'http://api.nbp.pl/api/exchangerates/rates/a/'

    data_grouped = data.groupby(['currency', 'booking_date']).size().reset_index().drop([0], axis=1)
    currency_date = data_grouped.loc[data_grouped['currency'] != 'PLN']

    df_currency = pd.DataFrame()
    for index, row in currency_date.iterrows():
        currency = row['currency']
        booking_date = row['booking_date'].strftime('%Y-%m-%d')

        url = base_url + currency + '/' + booking_date

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("General Error", err)
        else:
            currency = json_normalize(r.json()['rates'])
            currency['currency'] = row['currency']
            currency = currency.drop(columns='no')
            df_currency = df_currency.append(currency)
    return df_currency


def transform_data(data, df_currency):
    data['booking_date'] = pd.to_datetime(data["booking_date"])
    df_currency['effectiveDate'] = pd.to_datetime(df_currency["effectiveDate"])

    merged = pd.merge(data, df_currency, left_on=['booking_date', 'currency'], right_on=['effectiveDate', 'currency'],
                      how='left')
    merged['mid'] = merged['mid'].fillna(1)
    merged['price'] = merged['price'].astype(float)
    merged['price_pln'] = (merged['price'] * merged['mid']).round(2)
    merged['year_month'] = merged['booking_date'].dt.strftime('%Y-%m-01')
    merged = merged.drop(['price', 'currency', 'effectiveDate', 'mid', 'booking_date'], axis=1)
    return merged
