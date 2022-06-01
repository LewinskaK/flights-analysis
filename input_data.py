import pandas as pd
import psycopg2
import json


def get_data():
    c = open('connection.json')
    conn = json.load(c)
    c.close()

    username = conn['username']
    password = conn['password']
    host = conn['host']
    db = conn['db']

    try:
        connection = psycopg2.connect(
            host=host,
            database=db,
            user=username,
            password=password)

        cursor = connection.cursor()

        query = 'SELECT m.name as country_name, f.booking_date, f.reservation_number, f.price, f.currency \
        FROM flights.flights f LEFT JOIN flights.market_dictionary m on m.code=f.market_code '
        cursor.execute(query)
        flights = cursor.fetchall()
        cursor.close()
        data = pd.DataFrame(flights, columns=['country_name', 'booking_date', 'reservation_number', 'price', 'currency'])

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    else:
        if connection:
            cursor.close()
            connection.close()
        return data
