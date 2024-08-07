import requests
import random
import csv
import os

# Configuration
LOCATION = 'Oslo'
LATITUDE = 59.91
LONGITUDE = 10.75
TEMPERATURE_RANGES = {
    'hot': (25, float('inf')),
    'warm': (15, 24.9),
    'cool': (5, 14.9),
    'cold': (-5, 4.9),
    'very_cold': (-15, -5.1),
    'freezing': (float('-inf'), -15.1),
}
RAIN_CATEGORY = 'rain'
WINDY_CATEGORY = 'windy'
CLOTHES_CSV = 'clothes_outerwear.csv'
WEATHER_CSV = 'weather_data.csv'
USER_AGENT = 'clothes-suggesting-app/1.0'

# Function to fetch weather data
def get_weather_data(lat, lon):
    url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}'
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to save weather data to CSV
def save_weather_data(weather_data):
    date = weather_data['properties']['timeseries'][0]['time']
    temp = weather_data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    feels_like_temp = weather_data['properties']['timeseries'][0]['data']['instant']['details'].get('feels_like_temperature', temp)
    precipitation = weather_data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']

    # Check if CSV file exists, write header if not
    file_exists = os.path.isfile(WEATHER_CSV)
    with open(WEATHER_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['date', 'temperature', 'feels_like_temperature', 'precipitation'])
        writer.writerow([date, temp, feels_like_temp, precipitation])

# Function to load clothes data from CSV
def load_clothes_data(CLOTHES_CSV):
    clothes_data = []
    try:
        with open(CLOTHES_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                clothes_data.append(row)
    except FileNotFoundError:
        print(f"Error: The file {CLOTHES_CSV} does not exist.")
    return clothes_data

# Function to suggest clothes based on weather
def suggest_clothes_for_weather(temp, feels_like, precipitation, clothes_data):
    suitable_tops = []
    suitable_bottoms = []
    suitable_outerwear = []

    # Check for rain
    if 'rain' in precipitation.lower():
        print("It's raining, looking for rain gear.")
        suitable_tops = [item for item in clothes_data if item['Type'] == 'top' and item['Category'] == RAIN_CATEGORY]
        suitable_bottoms = [item for item in clothes_data if item['Type'] == 'bottom' and item['Category'] == RAIN_CATEGORY]
        suitable_outerwear = [item for item in clothes_data if item['Type'] == 'outerwear' and item['Category'] == RAIN_CATEGORY]

        # If no rain-specific tops, consider any available tops
        if not suitable_tops:
            suitable_tops = [item for item in clothes_data if item['Type'] == 'top']
    else:
        effective_temp = min(temp, feels_like)
        for key, (min_temp, max_temp) in TEMPERATURE_RANGES.items():
            if min_temp <= effective_temp <= max_temp:
                suitable_tops.extend([item for item in clothes_data if item['Type'] == 'top' and item['Category'] == key])
                suitable_bottoms.extend([item for item in clothes_data if item['Type'] == 'bottom' and item['Category'] == key])
                suitable_outerwear.extend([item for item in clothes_data if item['Type'] == 'outerwear' and item['Category'] == key])

    # Ensure that we have suitable clothing in all categories
    if not suitable_tops:
        print("No suitable tops found for current weather.")
        suitable_tops = [item for item in clothes_data if item['Type'] == 'top']
    if not suitable_bottoms:
        print("No suitable bottoms found for current weather.")
        suitable_bottoms = [item for item in clothes_data if item['Type'] == 'bottom']
    if not suitable_outerwear:
        print("No suitable outerwear found for current weather.")
        suitable_outerwear = [item for item in clothes_data if item['Type'] == 'outerwear']

    # Randomly select items from the suitable clothing
    chosen_top = random.choice(suitable_tops) if suitable_tops else None
    chosen_bottom = random.choice(suitable_bottoms) if suitable_bottoms else None
    chosen_outerwear = random.choice(suitable_outerwear) if suitable_outerwear else None

    return chosen_top, chosen_bottom, chosen_outerwear

# Main function
def main():
    clothes_data = load_clothes_data(CLOTHES_CSV)
    
    if not clothes_data:
        print("No clothes data available. Please ensure the clothes.csv file exists and is properly formatted.")
        return
    
    # Fetch weather data
    weather_data = get_weather_data(LATITUDE, LONGITUDE)
    if weather_data:
        save_weather_data(weather_data)
        temp = weather_data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
        feels_like = weather_data['properties']['timeseries'][0]['data']['instant']['details'].get('feels_like_temperature', temp)
        precipitation = weather_data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']
        
        # Print the weather data
        print(f"Current weather in {LOCATION}:")
        print(f"- Temperature: {temp}°C")
        print(f"- Feels Like: {feels_like}°C")
        print(f"- Precipitation: {precipitation}")

        # Suggest clothes
        top, bottom, outerwear = suggest_clothes_for_weather(temp, feels_like, precipitation, clothes_data)
        if top and bottom and outerwear:
            print(f"Suggested outfit for today in {LOCATION}:")
            print(f"- Top: {top['Item']}")
            print(f"- Bottom: {bottom['Item']}")
            print(f"- Outerwear: {outerwear['Item']}")
        else:
            print("No suitable clothes found for current weather.")
    else:
        print("Weather data could not be fetched.")

if __name__ == "__main__":
    main()
