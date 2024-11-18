import requests
import matplotlib.pyplot as plt
from dateutil.parser import parse
import pandas as pd
import seaborn as sns

plt.rcParams.update({'font.size': 22})

# What we want to do:
# 1. Adapt functions from week 7 workshop to return Pandas dataframe
# 2. Simplify a little
# 3. Manipulate the resulting dataframe to make it work well with Seaborn
#    (convert to long format (melt), joining/merging dataframes)


def get_weather_data(city_name, frequency, variables):
    # Get city information
    params_dict = {'name': city_name, 'count': 1}
    city_info = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params_dict).json()

    # Extract the first result in the list
    city_info = city_info['results'][0]

    # Get latitude, longitude, and time zone
    latitude, longitude = city_info['latitude'], city_info['longitude']
    time_zone = city_info['timezone']

    # Create a dictionary for the parameters I need
    params_dict = {'timezone': time_zone,
                   'latitude': latitude,
                   'longitude': longitude,
                   frequency: variables}
    
    # print(latitude, longitude)

    # Request data from the API
    r = requests.get('https://api.open-meteo.com/v1/forecast', params=params_dict)

    # Parse the JSON data to a dictionary
    data = pd.DataFrame(r.json()['hourly'])
    data['time'] = pd.to_datetime(data['time'])

    return data

    # print(data)
    # data.info()

    # # Start an empty dictionary, populate the timestamps parsed as datetime objects
    # weather_dict = {'timestamps': [parse(t) for t in data[frequency]['time']]}

    # # Start a dictionary item to store the units
    # # weather_dict['units'] = {var: data[f'{frequency}_units'][var] for var in variables}

    # # Extract the data, add to dictionary
    # for var in variables:
    #     weather_dict[var] = data[frequency][var]

    # Return the data
    # return weather_dict


# def weather_forecast(city_name):
#     '''
#     Retrieves and displays a weather forecast for city_name.
#     '''
#     params_dict = {'name': city_name, 'count': 1}
#     city_info = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params_dict).json()

#     # Extract the first result in the list
#     city_info = city_info['results'][0]

#     # Get latitude, longitude, and time zone
#     latitude, longitude = city_info['latitude'], city_info['longitude']
#     time_zone = city_info['timezone']

#     # Create a dictionary for the parameters I need
#     frequency = 'hourly'
#     params_dict = {'timezone': time_zone,
#                    'latitude': latitude,
#                    'longitude': longitude,
#                    frequency: ['cloudcover' ,'temperature_2m']}

#     # Display the weather forecast
#     r = requests.get('https://api.open-meteo.com/v1/forecast', params=params_dict)
#     weather_dict = get_weather_data(r, frequency, params_dict[frequency])
#     fig, ax = display_weather_data(weather_dict)
#     ax[0].set_title(f'Weather forecast in {city_name}')
#     plt.show()


if __name__ == '__main__':
    city_name = 'Edinburgh'
    frequency = 'hourly'
    variables = ['temperature_2m', 'cloud_cover']
    weather_data = get_weather_data(city_name, frequency, variables)
    # print(weather_data.head(20))

    # # Plot just the temperature data over time
    # sns.relplot(data=weather_data, x='time', y='temperature_2m', kind='line')
    # plt.show()

    # sns.relplot(data=weather_data, x='time', y='temperature_2m', hue='cloud_cover', size='cloud_cover')
    # plt.show()

    # Plot temperature and cloud cover in 2 separate subplots

    # First: convert to long format
    weather_data = pd.melt(weather_data, id_vars=['time'], value_vars=['temperature_2m', 'cloud_cover'])
    # print(weather_data)

    sns.relplot(data=weather_data, x='time', y='value', col='variable')
    plt.show()

    # Exercises:
    # - Add more weather variables
    # - Incorporate the units in the labels/titles
    # - Get data for another city, merge it with first city, plot
    #     data for the 2 cities in the same figure