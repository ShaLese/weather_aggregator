import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json

# Kenya cities coordinates (approximate)
KENYA_CITIES_COORDS = {
    'Nairobi': (-1.2921, 36.8219),
    'Mombasa': (-4.0435, 39.6682),
    'Kisumu': (-0.1022, 34.7617),
    'Nakuru': (-0.3031, 36.0800),
    'Eldoret': (0.5143, 35.2698),
    'Malindi': (-3.2138, 40.1169),
    'Kitale': (1.0187, 35.0062),
    'Garissa': (-0.4536, 39.6401),
    'Thika': (-1.0396, 37.0900),
    'Kakamega': (0.2827, 34.7519)
}

def load_data():
    """Load and prepare the weather data"""
    df = pd.read_csv('kenya_cities.csv')
    
    # Clean up the data
    df['temperature'] = df['temperature'].str.replace('°C', '').astype(float)
    df['humidity'] = df['humidity'].str.replace('%', '').astype(float)
    df['wind_speed'] = df['wind_speed'].str.replace(' km/h', '').astype(float)
    
    return df

def create_map(df):
    """Create a folium map with weather information"""
    # Create a map centered on Kenya
    m = folium.Map(location=[-0.0236, 37.9062], zoom_start=6)
    
    for city in df.itertuples():
        if city.city in KENYA_CITIES_COORDS:
            lat, lon = KENYA_CITIES_COORDS[city.city]
            
            # Create popup content
            popup_content = f"""
                <div style='width: 200px'>
                    <h4>{city.city}</h4>
                    <p><b>Temperature:</b> {city.temperature}°C</p>
                    <p><b>Humidity:</b> {city.humidity}%</p>
                    <p><b>Wind Speed:</b> {city.wind_speed} km/h</p>
                    <p><b>Condition:</b> {city.condition}</p>
                </div>
            """
            
            # Add marker with popup
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{city.city}: {city.temperature}°C",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    return m

def main():
    st.set_page_config(
        page_title="Kenya Weather Dashboard",
        page_icon="🌦️",
        layout="wide"
    )
    
    # Title and description
    st.title("🌦️ Kenya Weather Dashboard")
    st.markdown("Real-time weather information for major cities in Kenya")
    
    # Load the data
    df = load_data()
    
    # Display last update time
    last_update = pd.to_datetime(df['last_updated'].iloc[0])
    st.sidebar.write("Last Updated:", last_update.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Highest Temperature",
            f"{df['temperature'].max():.1f}°C",
            f"in {df.loc[df['temperature'].idxmax(), 'city']}"
        )
    
    with col2:
        st.metric(
            "Lowest Temperature",
            f"{df['temperature'].min():.1f}°C",
            f"in {df.loc[df['temperature'].idxmin(), 'city']}"
        )
    
    with col3:
        st.metric(
            "Average Temperature",
            f"{df['temperature'].mean():.1f}°C",
            "across all cities"
        )
    
    # Create two columns for the map and charts
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📍 Weather Map")
        m = create_map(df)
        folium_static(m)
    
    with col2:
        st.subheader("📊 Temperature Distribution")
        fig = px.bar(
            df,
            x='city',
            y='temperature',
            color='temperature',
            color_continuous_scale='RdYlBu_r',
            labels={'temperature': 'Temperature (°C)', 'city': 'City'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Create two columns for humidity and wind speed
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💧 Humidity Levels")
        fig = px.bar(
            df,
            x='city',
            y='humidity',
            color='humidity',
            color_continuous_scale='Blues',
            labels={'humidity': 'Humidity (%)', 'city': 'City'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌪️ Wind Speed")
        fig = px.bar(
            df,
            x='city',
            y='wind_speed',
            color='wind_speed',
            color_continuous_scale='Viridis',
            labels={'wind_speed': 'Wind Speed (km/h)', 'city': 'City'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed data table
    st.subheader("📋 Detailed Weather Data")
    st.dataframe(
        df.style.format({
            'temperature': '{:.1f}°C',
            'humidity': '{:.1f}%',
            'wind_speed': '{:.1f} km/h'
        }),
        hide_index=True
    )

if __name__ == "__main__":
    main()
