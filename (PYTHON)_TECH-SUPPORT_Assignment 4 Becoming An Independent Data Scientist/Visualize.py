import pandas as pd
import matplotlib.pyplot as plt

# Refernce for confirmed cases
confirmed_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

# Top 5 Populated Countries
countries = ("China","India","Indonesia","Pakistan","Bangladesh")

# (from,to)
timeframe = ('2020-01-22','2021-09-8')

# Moving Average
MA = 30


# Parse Dates
dates = confirmed_df.columns[4:]

full_table = confirmed_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
    value_vars=dates,
    var_name='Date',
    value_name='Confirmed'
)

print(full_table)

full_table['Date'] = pd.to_datetime(full_table['Date'])

full_table['Date'] = full_table['Date'][(full_table['Date'] > timeframe[0]) & (full_table['Date'] < timeframe[1])]

full_grouped = full_table.groupby(['Date', 'Country/Region'])['Confirmed'].sum().reset_index()

for x in countries:
    full_grouped_filtered = full_grouped[full_grouped['Country/Region'] == x]
    full_grouped_filtered_MA = full_grouped_filtered['Confirmed'].rolling(window = MA).mean()
    plt.plot(full_grouped_filtered['Date'],full_grouped_filtered_MA,linestyle='solid',linewidth=1)
    plt.fill_between(full_grouped_filtered['Date'],full_grouped_filtered_MA, alpha=0.5)

plt.legend(countries)
plt.title("Top 5 Populated Asean Countries Confirmed Cases")
plt.xlabel("Date")
plt.ylabel("30 Days Moving Average Confirmed Cases(Person)")
plt.tight_layout()
plt.xticks(rotation=50)

plt.show()
