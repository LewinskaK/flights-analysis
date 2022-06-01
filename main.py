from input_data import get_data
from analysis import analysis
from exchange_rates import get_exchange_rates, transform_data


def run():
    data = get_data()
    df_currency = get_exchange_rates(data)
    merged = transform_data(data, df_currency)
    analysis(merged)


if __name__ == "__main__":
    run()
