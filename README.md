# Kenya Weather Data Aggregator

A comprehensive weather tracking system for Kenyan cities with automated data collection and interactive visualization.

## Project Overview

This project provides real-time weather monitoring for major cities in Kenya, featuring:
- Automated data collection from WeatherAPI.com
- Detailed logging of operations and updates
- Interactive web dashboard with visualizations
- Support for 10 major Kenyan cities

## Features

### 1. Data Collection
- **API**: WeatherAPI.com (Free tier - 1 million monthly API calls)
- **Cities Monitored**:
  - Nairobi
  - Mombasa
  - Kisumu
  - Nakuru
  - Eldoret
  - Malindi
  - Kitale
  - Garissa
  - Thika
  - Kakamega
- **Weather Metrics**:
  - Temperature (°C)
  - Humidity (%)
  - Wind Speed (km/h)
  - Weather Condition
  - Last Updated Timestamp

### 2. Data Storage
- CSV format (`kenya_cities.csv`)
- Columns:
  - city
  - temperature
  - humidity
  - wind_speed
  - condition
  - last_updated

### 3. Logging System
- Log file: `weather_updates.log`
- Tracks:
  - API requests
  - Data updates
  - Error messages
  - Operation timestamps

### 4. Interactive Dashboard
- Built with Streamlit
- Features:
  - Interactive Kenya map with city markers
  - Temperature distribution charts
  - Humidity level visualizations
  - Wind speed comparisons
  - Key weather metrics
  - Detailed data table

## Setup and Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your WeatherAPI.com API key:
   - Sign up at [WeatherAPI.com](https://www.weatherapi.com)
   - Get your API key
   - Add it to `weather_scraper.py`

## Usage

1. Run the weather scraper:
```bash
python weather_scraper.py
```

2. Launch the dashboard:
```bash
streamlit run dashboard.py
```

## Dependencies

- Python 3.11+
- pandas
- requests
- streamlit
- plotly
- folium
- streamlit-folium

## Project Structure

- `weather_scraper.py`: Data collection script
- `dashboard.py`: Streamlit dashboard application
- `kenya_cities.csv`: Weather data storage
- `weather_updates.log`: Operation logs
- `requirements.txt`: Project dependencies

## Development Notes

### Current Limitations
- Relies on external API availability
- Free tier API rate limits
- Manual API key management required

### Future Improvements
- Automated scheduling of data updates
- Enhanced error handling
- Additional weather metrics
- Historical data tracking
- More cities coverage

## Security Notes
- API key should be stored as an environment variable in production
- No sensitive personal data is handled

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).
