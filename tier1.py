#main.py 
##run the data with the command: python3 main.py
#1. Sourcing and Loading
#1.1 Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#1.2 Loading the data
#load the data from London DataStore
url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)

#2. Cleaning, Transforming, and Visualizing: Rows are the observations and columns are variables

#2.1 Explore the data
print(properties.shape)
#print(properties)
#print(properties.head())

#2.2 Cleaning the data
properties_T = properties.transpose()
#print(properties_T.shape)
#print(properties_T)
properties = properties_T.reset_index()
print(properties.shape)
#print(properties.head())
#print(properties.columns)

#2.3 Cleaning the data
properties.columns = properties.iloc[0]
properties = properties.drop(0)
print("Hello World")
properties = properties.rename(columns = {'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})
print(properties)
print("hello World")

#2.4 Transforming the data
properties = pd.melt(properties, id_vars= ['London_Borough', 'ID'])
properties = properties.rename(columns = {0: 'Month', 'value': 'Average_price'})
properties['Average_price'] = pd.to_numeric(properties['Average_price'])

#2.5 Cleaning the data
properties = properties.dropna()
# A list of non-boroughs. 
nonBoroughs = ['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']
properties = properties[~properties.London_Borough.isin(nonBoroughs)]
print(properties)

#2.6 Visualizing the data
# Restrict your observations to Camden for now. How have housing prices changed since 1995?
camden_prices = properties[properties['London_Borough'] == 'Camden']
ax = camden_prices.plot(kind='line', x = 'Month', y = 'Average_price')
ax.set_ylabel('Price')
plt.show()

properties['Year'] = properties['Month'].apply(lambda t: t.year)
print(properties.tail())

dfg = properties.groupby(by=['London_Borough', 'Year']).mean()
print(dfg.sample(10))

dfg = dfg.reset_index()
print(dfg.head())

# 3. Modelling
# create a function that will calculate a ratio of house prices, 
# that compares the price of a house in 2018 to the price in 1998.
# Call this function create_price_ratio
# dfg[dfg['London_Borough']=='Camden']
# Get the Average Price for that borough for 1998 and, separately, for 2018.
# Calculate the ratio of the Average Price for 1998 divided by the Average Price for 2018.
# Return that ratio.

def create_price_ratio(d):
    y1998 = float(d['Average_price'][d['Year']==1998])
    y2018 = float(d['Average_price'][d['Year']==2018])
    ratio = [y2018/y1998]
    return ratio

# Example
create_price_ratio(dfg[dfg['London_Borough']=='Barking & Dagenham'])

final = {} #dictionary with data = the ratio of average prices for each borough between 1998 and 2018
for b in dfg['London_Borough'].unique():
	borough = dfg[dfg['London_Borough'] == b]
	final[b] = create_price_ratio(borough)
	print(b, final[b], "\n")

# Make the dictionary into a DataFrame
df_ratios = pd.DataFrame(final)
#print(df_ratios.head())

df_ratios = df_ratios.transpose()
df_ratios = df_ratios.reset_index()
df_ratios.rename(columns={'index':'Borough', 0:'2018'}, inplace=True)
print(df_ratios.head())

# Let's sort in descending order and select the top 15 boroughs.
top15 = df_ratios.sort_values(by='2018',ascending=False)
print(top15.head(15))

# Let's plot the boroughs that have seen the greatest changes in price.
ax = top15[['Borough','2018']].plot(kind='bar')
ax.set_xticklabels(top15.Borough)
plt.show()
