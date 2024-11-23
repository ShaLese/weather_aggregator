import pandas as pd
import requests
from datetime import datetime
import time
import json

class WeatherScraper:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.api_key = "80beadc6a569457ea3d82440242311"
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        self.log_file = "weather_updates.log"
        
    def log_message(self, message):
        """Write a message to the log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp} - {message}\n")
        
    def get_location_data(self, city):
        """Get weather data for a specific city using WeatherAPI.com"""
        try:
            # Create the URL with parameters
            params = {
                'q': f"{city},Kenya",
                'key': self.api_key,
            }
            
            self.log_message(f"Making API request for {city}")
            # Get the data
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            weather_data = {
                'temperature': f"{data['current']['temp_c']}°C",
                'humidity': f"{data['current']['humidity']}%",
                'wind_speed': f"{data['current']['wind_kph']} km/h",
                'condition': data['current']['condition']['text'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.log_message(f"Weather data for {city}: Temp={weather_data['temperature']}, Humidity={weather_data['humidity']}, Wind={weather_data['wind_speed']}, Condition={weather_data['condition']}")
            return weather_data
            
        except Exception as e:
            error_msg = f"Error getting data for {city}: {str(e)}"
            self.log_message(error_msg)
            print(error_msg)
            return None

    def update_weather_data(self):
        """Update weather data for all cities in the CSV"""
        try:
            self.log_message("Starting weather data update process")
            # Read the CSV file
            df = pd.read_csv(self.csv_file)
            self.log_message(f"Found {len(df)} cities in the CSV file")
            
            # Create empty lists for new data
            temperatures = []
            humidities = []
            wind_speeds = []
            conditions = []
            timestamps = []
            
            # Get weather data for each city
            for city in df['city']:
                print(f"Getting weather data for {city}...")
                weather_data = self.get_location_data(city)
                
                if weather_data:
                    temperatures.append(weather_data['temperature'])
                    humidities.append(weather_data['humidity'])
                    wind_speeds.append(weather_data['wind_speed'])
                    conditions.append(weather_data['condition'])
                    timestamps.append(weather_data['timestamp'])
                else:
                    self.log_message(f"No data available for {city}, using N/A values")
                    temperatures.append('N/A')
                    humidities.append('N/A')
                    wind_speeds.append('N/A')
                    conditions.append('N/A')
                    timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                
                # Add delay to avoid hitting rate limits
                time.sleep(1)
            
            # Update the DataFrame
            df['temperature'] = temperatures
            df['humidity'] = humidities
            df['wind_speed'] = wind_speeds
            df['condition'] = conditions
            df['last_updated'] = timestamps
            
            # Save the updated data
            df.to_csv(self.csv_file, index=False)
            self.log_message("Weather data updated successfully!")
            print("Weather data updated successfully!")
            
        except Exception as e:
            error_msg = f"Error updating weather data: {str(e)}"
            self.log_message(error_msg)
            print(error_msg)

if __name__ == "__main__":
    print("Weather Data Scraper")
    print("===================")
    print("Starting weather data collection...")
    scraper = WeatherScraper('kenya_cities.csv')
    scraper.update_weather_data()
