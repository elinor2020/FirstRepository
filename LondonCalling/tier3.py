# London Calling Tier 3
# Run: python3 tier3.py

# 1.1 Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1.2 Loading the data from London Datastore
url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)

# 2. Cleaning, transforming, and visualizing
# The end goal of data cleaning is to have tidy data:
# Each variable has a column.
# Each observation forms a row.

# 2.1 Exploring the data
#print(properties.shape)
#print(properties.head())

# 2.2 Cleaning the data (Part 1)
properties = properties.transpose()
#print(properties.head())

# Confirm what are the row indices
#print(properties.index)
# reset the indices
properties = properties.reset_index()
#print(properties.head())
# Confirm that the columns are mainly integers
#print(properties.columns)

# Confirm the first row contains the proper values for column headings
#print(properties.iloc[[0]])

# Need to drop the row at index 0:
properties.columns = properties.iloc[0]
properties = properties.drop(0)
#print(properties.head())

# 2.3 Cleaning the data (Part 2)
properties = properties.rename(columns = {'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})
#print(properties)

# How many columns?
#print(properties.columns)

# 2.4 Transforming the data
# Melt those values along the column headings of our current DataFrame into a single column.
properties = pd.melt(properties, id_vars= ['London_Borough', 'ID'])

# Rename the column names
properties = properties.rename(columns = {0: 'Month', 'value': 'Average_price'})
#print(properties.head())

# Change the Average_price column to a numeric type, a float.
#print(properties.dtypes)
properties['Average_price'] = pd.to_numeric(properties['Average_price'])
#print(properties.dtypes)

# Count NaNs
#print('Missing Values')
#print(properties.isna().sum())

# 2.5 Cleaning the data (Part 3)
# Since there are only 32 London boroughs, check out the unique values of 
# the 'London_Borough' column to see if they're all there.
# unique = properties['London_Borough'].unique()
#print(unique)

# Filtering the data with NaN values
propertiesD = properties.dropna()
#print(propertiesD.head(33))
#print(propertiesD['London_Borough'].unique())
#print(propertiesD.count())
#print(propertiesD.shape)
#print(propertiesD.shape)

# A list of non-boroughs. 
nonBoroughs = ['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']

# Drop the nonBoroughs
df = propertiesD[~propertiesD.London_Borough.isin(nonBoroughs)]
#print(df.head())
#print(df.dtypes)

# 2.6 Visualizing the data
camden_prices = df[df['London_Borough'] == 'Hounslow']
#camden_prices = df[df['London_Borough'] == 'Barking & Dagenham']
#ax = camden_prices.plot(kind = 'line', x = 'Month', y = 'Average_price')
#plt.title('Hounslow')
#ax.set_ylabel('Price')
#plt.show()

# To limit the amount of temporal data-points, it's useful 
# to extract the year from every value in your Month column.
# Apply the lambda function:
# 1. look through the Month column
# 2. extract the year from each individual value in that column
# 3. store that corresponding year as separate column

# The following line throws a warning. How to fix?
df['Year'] = df['Month'].apply(lambda t: t.year)

# print(df.tail())

# Calculate the mean for each year and for each Borough
df = df.groupby(by=['London_Borough', 'Year']).mean()
#print(df.sample(10))
df = df.reset_index()
#print(df.head(10))

# 3. Modeling
# function "create_price_ratio" will calculate a ratio of house prices, 
# that compares the price of a house in 2018 to the price in 1998.

def create_price_ratio(d):
    y1998 = float(d['Average_price'][d['Year']==1998])
    y2018 = float(d['Average_price'][d['Year']==2018])
    ratio = [y1998/y2018]
    return ratio

# test the function:
#print(create_price_ratio(df[df['London_Borough']=='Hounslow']))

# Store ratios for each unique London_Borough:
final = {}

# for loop iterates through each of the unique elements of the 'London_Borough' column:
for b in df['London_Borough'].unique():
	borough = df[df['London_Borough'] == b]
	final[b] = create_price_ratio(borough)
#print(final)

df_ratios = pd.DataFrame(final)
# print(df_ratios.head())

df = df_ratios.transpose()
df = df.reset_index()
# print(df)

df.rename(columns={'index':'Borough', 0:'2018'}, inplace=True)
# print(df)

# Sort in descending order and select the top 15 boroughs
top15 = df.sort_values(by='2018',ascending=False)
print(top15.head(32))

# Plot the boroughs that have seen the greatest changes in price
ax = top15[['Borough','2018']].plot(kind='bar')
ax.set_xticklabels(top15.Borough)
plt.title('1998/2018 Price Ratio for London Boroughs')
plt.show()
