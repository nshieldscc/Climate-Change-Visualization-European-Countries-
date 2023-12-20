# import necessary modules
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# open the pickle file to be used
file = open('countrytempdata', 'rb')
annual_averages_12monthyears = pickle.load(file)

# reformat as a dataframe so plots can be made
df_annual_averages_12monthyears = pd.DataFrame(annual_averages_12monthyears)
df_annual_averages_12monthyears = df_annual_averages_12monthyears.sort_index()

# function that creates and saves a moving-average plot given a country
def display_plot(country):
    window_size = 10
    df_annual_averages_12monthyears[f'Moving Average {country}'] = \
    df_annual_averages_12monthyears[country].rolling(window=window_size).mean()
    
    fig, ax = plt.subplots(figsize=(50, 20))
    

    plt.plot(df_annual_averages_12monthyears.index, \
             df_annual_averages_12monthyears[f'Moving Average {country}'], \
             marker='o', linewidth=6)

    plt.xlabel('Year',fontsize=35, weight='bold')
    plt.ylabel('Moving Annual Average Temperature (Window = 10)', \
               fontsize=35, weight='bold')
    plt.xticks(rotation=75, fontsize=10)
    plt.yticks(fontsize=20)
    plt.title(f'{country} (Moving Average)', fontsize=45, weight='bold')

    plt.savefig(f'{country}')
    plt.clf()
    plt.close()
    
# specify relevant countries
countries = ["Iceland",
"Norway",
"Sweden",
"Finland",
"United Kingdom",
"Ireland",
"Portugal",
"Spain",
"France",
"Belgium",
"Netherlands",
"Germany",
"Switzerland",
"Italy",
"Poland",
"Austria",
"Slovakia",
"Hungary",
"Slovenia",
"Croatia",
"Bosnia And Herzegovina",
"Serbia",
"Romania",
"Bulgaria",
"Czech Republic",
"Estonia",
"Latvia",
"Lithuania",
"Belarus",
"Moldova",
"Ukraine",
"Denmark",
"Montenegro",
"Albania",
"Greece",
"Turkey"]

# run the function for all the countries
for country in countries:
    display_plot(country)
    
# verify completion!
print('Done')