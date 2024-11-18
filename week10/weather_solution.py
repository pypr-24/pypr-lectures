import requests
import matplotlib.pyplot as plt
from dateutil.parser import parse

# Task 1

# Request information using online URL builder interface
r = requests.get('https://api.open-meteo.com/v1/forecast?latitude=55.9&longitude=-3.2&hourly=temperature_2m,precipitation&timezone=Europe%2FLondon')
#  print(r.json())

# NOTE: doing this with Pandas is probably a lot easier! Revisit this in a couple of weeks...
# Convenience function for extracting data from a JSON request
def get_weather_data(r, frequency, variables):
    '''
    Returns only the required data from a JSON request.
    The result is a dictionary in the form:
    {'units': {variables[0]: unit, variables[1]: unit, ...},
     'variables[0]': [.., .., .., ..],
     'variables[1]': [.., .., .., ..],
     ...}

    Input:
        r (Request): the request object
        frequency (str): 'hourly' or 'daily'.
        variables (list): a list of the required variable names.

    Output:
        weather_dict (dict): a dictionary containing only the required data.
    '''
    # Parse the JSON data to a dictionary
    data = r.json()

    # Start an empty dictionary, populate the timestamps parsed as datetime objects
    weather_dict = {'timestamps': [parse(t) for t in data[frequency]['time']]}

    # Start a dictionary item to store the units
    weather_dict['units'] = {var: data[f'{frequency}_units'][var] for var in variables}

    # Extract the data, add to dictionary
    for var in variables:
        weather_dict[var] = data[frequency][var]

    # Return the data
    return weather_dict


# Convenience function to plot the results
def display_weather_data(weather_dict, same_plot=False):
    '''
    Plots the required weather data.

    Input:
        weather_dict (dict): output from get_weather_data().
        same_plot (bool, default False): display on the same graph or not.

    Output: figure and axes.
    '''
    # Get list of variables
    variables = list(weather_dict.keys())
    variables = [var for var in variables if var not in ['timestamps', 'units']]
    num_vars = len(variables)

    # Total number of subplots
    num_plots = 1 if same_plot else num_vars

    # Create figure and axes
    fig, ax = plt.subplots(num_plots, 1)

    # Plot each variable over time (except units and time itself)
    for i in range(num_vars):
        # Current axis
        if same_plot:
            current_ax = ax
        else:
            current_ax = ax[i]

        current_ax.plot(weather_dict['timestamps'], weather_dict[variables[i]])

        # Format the axes
        ylabel = f'{variables[i]} ({weather_dict["units"][variables[i]]})'
        current_ax.set(xlabel='Date', ylabel=ylabel)
        current_ax.xaxis_date()

    return fig, ax


# Display the results of the request
weather_dict = get_weather_data(r, 'hourly', ['temperature_2m','precipitation'])
fig, ax = display_weather_data(weather_dict)
plt.show()



# Task 1: simplified

# Request information using online URL builder interface
r = requests.get('https://api.open-meteo.com/v1/forecast?latitude=55.9&longitude=-3.2&hourly=temperature_2m,precipitation&timezone=Europe%2FLondon')

# Parse the JSON data to a dictionary
data = r.json()

# Get the time, temperature, and precipitation
timestamps = data['hourly']['time']
temperature = data['hourly']['temperature_2m']
precipitation = data['hourly']['precipitation']

# Plot the data
fig, ax = plt.subplots(2, 1)

# Plot temperature and precipitation over time
ax[0].plot(timestamps, temperature)
ax[1].plot(timestamps, precipitation)

# Format the axes
ylabels = ['Temperature (C)', 'Precipitation (mm)']

for i in range(2):
    # Set axis labels
    ax[i].set(xlabel='Date', ylabel=ylabels[i])

    # Only display x-tick every 24 hours
    ax[i].set_xticks(ax[i].get_xticks()[::24])

plt.show()



# Task 2

# Create a dictionary for the parameters I need
frequency = 'daily'
params_dict = {'timezone': 'Europe/London',
               'latitude': 55.9,
               'longitude': -3.2,
               frequency: ['temperature_2m_max' ,'temperature_2m_min']}

# Make a request by passing these parameters
r = requests.get('https://api.open-meteo.com/v1/forecast', params=params_dict)

# Display the results
weather_dict = get_weather_data(r, frequency, params_dict[frequency])
fig, ax = display_weather_data(weather_dict, same_plot=True)
plt.show()



# Task 3

def weather_forecast(city_name):
    '''
    Retrieves and displays a weather forecast for city_name.
    '''
    params_dict = {'name': city_name, 'count': 1}
    city_info = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params_dict).json()

    # Extract the first result in the list
    city_info = city_info['results'][0]

    # Get latitude, longitude, and time zone
    latitude, longitude = city_info['latitude'], city_info['longitude']
    time_zone = city_info['timezone']

    # Create a dictionary for the parameters I need
    frequency = 'hourly'
    params_dict = {'timezone': time_zone,
                   'latitude': latitude,
                   'longitude': longitude,
                   frequency: ['cloudcover' ,'temperature_2m']}

    # Display the weather forecast
    r = requests.get('https://api.open-meteo.com/v1/forecast', params=params_dict)
    weather_dict = get_weather_data(r, frequency, params_dict[frequency])
    fig, ax = display_weather_data(weather_dict)
    ax[0].set_title(f'Weather forecast in {city_name}')
    plt.show()

weather_forecast('Caen')
