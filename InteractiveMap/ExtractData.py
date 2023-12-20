# import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# import file and read
transactionfile = 'GlobalLandTemperaturesByCountry.csv'
df_country = pd.read_csv(transactionfile)

# optionally inspect the structure of the data
#df_country.head()

# sort the unique countries
unique_countries = sorted(df_country['Country'].unique())

# look at the dataframe's 'head' and drop the unnecessary columns
# 'dropna' drops all the NaN (null) values
df_country = df_country.drop('AverageTemperatureUncertainty', \
                             axis=1).dropna().reset_index(drop=True)

# parse the data into a dictionary that can be used in the other py files
# initialize counts, indexes, initial values, and dictionary
row_count = len(df_country)
row_index = 0
avg_temp_sum = 0
avg_temp_count = 1
annual_averages_12monthyears = {}

row = df_country.iloc[0]
date_contents = row['dt'].split('-')
year = date_contents[0]
previous_year = year

country = row['Country']
previous_country = country

# loop through all the rows in the data frame
for row in range(0, row_count):
    row = df_country.iloc[row_index]

    # collect the country, year, and avg temp from row
    country = row['Country']
    if country not in annual_averages_12monthyears:
        annual_averages_12monthyears[country] = {}
    date_contents = row['dt'].split('-')
    year = date_contents[0]
    avg_temp = row['AverageTemperature']

    #add the avg temp
    avg_temp_sum += avg_temp

    # if the year is different, add the year's data and reset sum and count
    if year != previous_year:
        row = df_country.iloc[row_index-1]
        country = row['Country']
        
        # go back in values to finalize the previous set
        avg_temp_count -= 1
        avg_temp_sum -= avg_temp

        # only add if there are 12 months in that year
        if avg_temp_count == 12:
            annual_avg = avg_temp_sum / avg_temp_count
            annual_avg = round(annual_avg, 2)
            annual_averages_12monthyears[country][previous_year] = annual_avg
        
        avg_temp_sum = 0
        avg_temp_count = 1
        
        # put the row values back to what they were before adding previous
        row = df_country.iloc[row_index]

        # collect the country, year, and avg temp from row
        country = row['Country']
        if country not in annual_averages_12monthyears:
            annual_averages_12monthyears[country] = {}
        date_contents = row['dt'].split('-')
        year = date_contents[0]
        avg_temp = row['AverageTemperature']
        
        #add the avg temp and increase the temp count by 1
        avg_temp_sum += avg_temp
    
    # set the 'previous year' and increase row_index by 1
    previous_year = year
    row_index += 1
    avg_temp_count += 1
    
# remove countries with problems (continents, countries with problem characters
# or duplicate countries)
list_to_remove = ['Åland','Denmark','France','Netherlands','United Kingdom',\
                  'Africa','Asia','Europe']
for country in list_to_remove:
    annual_averages_12monthyears.pop(country)
    
# rename the 'Europe' version of relevant countries to be the main version
annual_averages_12monthyears['Denmark'] = \
    annual_averages_12monthyears.pop('Denmark (Europe)')
annual_averages_12monthyears['France'] = \
    annual_averages_12monthyears.pop('France (Europe)')
annual_averages_12monthyears['Netherlands'] = \
    annual_averages_12monthyears.pop('Netherlands (Europe)')
annual_averages_12monthyears['United Kingdom'] = \
    annual_averages_12monthyears.pop('United Kingdom (Europe)')

# store the dictionary as a pickle file to be used in the other py files
with open('countrytempdata', 'wb') as file:
    pickle.dump(annual_averages_12monthyears, file)

# verify everything ran
print('Done')
