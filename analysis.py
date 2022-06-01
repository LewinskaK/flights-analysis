def analysis(merged):
    monthly_sales_sum = merged.groupby(['country_name', 'year_month']).sum() \
        .rename(columns={'price_pln': 'monthly_sales_sum'})
    print(f'\n\nMonthly sum of sales per country:\n {monthly_sales_sum}')
    monthly_sales_mean = merged.groupby(['country_name', 'year_month']).mean().round(2) \
        .rename(columns={'price_pln': 'monthly_sales_mean'})
    print(f'\n\nMonthly average sales per country:\n {monthly_sales_mean}')

    monthly_transaction_count = merged.groupby(['country_name', 'year_month'])[['price_pln']].count() \
        .rename(columns={'price_pln':'monthly_transaction_count'})
    print(f'\n\nMonthly number of transactions per country:\n {monthly_transaction_count}')

    monthly_max_transaction_value = merged.groupby(['country_name', 'year_month']).max() \
        .rename(columns={'price_pln': 'monthly_max_transaction_value'})
    print(f'\n\nMonthly maximum transaction value per country:\n {monthly_max_transaction_value}')
    monthly_min_transaction_value = merged.groupby(['country_name', 'year_month']).min() \
        .rename(columns={'price_pln': 'monthly_min_transaction_value'})
    print(f'\n\nMonthly minimum transaction value per country:\n {monthly_min_transaction_value}')

    min_transaction_value = merged[merged['price_pln'] == merged['price_pln'].min()]
    print(f'\n\nTransaction with the lowest amount:\n {min_transaction_value}')
    max_transaction_value = merged[merged['price_pln'] == merged['price_pln'].max()]
    print(f'\n\nTransaction with the highest amount:\n {max_transaction_value}')

    monthly_overall_sum = merged.groupby(['year_month']).sum() \
        .rename(columns={'price_pln': 'monthly_overall_sum'})
    monthly_overall_sum['month_to_month_difference'] = monthly_overall_sum.monthly_overall_sum.diff()
    print(f'\n\nMonthly sum of sales and the month-to-month difference:\n {monthly_overall_sum}')

