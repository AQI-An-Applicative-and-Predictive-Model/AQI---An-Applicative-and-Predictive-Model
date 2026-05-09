import pandas as pd
import numpy as np
import os

cities = [
    "Patna", "New Delhi", "Mumbai", "Gandhinagar", "Surat",
    "Chennai", "Kolkata", "Lucknow", "Bengaluru", "Ahmedabad",
    "Kanpur", "Jaipur", "Indore", "Nagpur", "Srinagar",
    "Thane", "Hyderabad", "Visakhapatnam", "Bhopal", "Pune"
]

# create folder
if not os.path.exists("Cities"):
    os.makedirs("Cities")

def generate_city_data(city):
    days = 30
    
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)

    pm10 = np.random.randint(80, 200, days)
    pm25 = np.random.randint(50, 150, days)
    ozone = np.random.randint(20, 60, days)

    # AQI calculation 
    aqi = (pm25 * 0.6 + pm10 * 0.4).astype(int)

    df = pd.DataFrame({
        "Date": dates,
        "PM 10": pm10,
        "PM 2.5": pm25,
        "AQI Value": aqi,
        "Ozone": ozone
    })

    df.to_csv(f"Cities/{city}_final.csv", index=False)
    print(f"{city} CSV created")

# generate all
for city in cities:
    generate_city_data(city)

print("All CSV files created successfully!")
