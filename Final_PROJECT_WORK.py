import pandas as pd
import os

def city_data(city):
    file_path = f"Cities/{city}_final.csv"
    
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    df = df.dropna()
    return df


cities = [
    "Patna", "New Delhi", "Mumbai", "Gandhinagar", "Surat",
    "Chennai", "Kolkata", "Lucknow", "Bengaluru", "Ahmedabad",
    "Kanpur", "Jaipur", "Indore", "Nagpur", "Srinagar",
    "Thane", "Hyderabad", "Visakhapatnam", "Bhopal", "Pune"
]


#  function to get all cities data
def get_all_cities_data():
    all_data = {}

    for city in cities:
        df = city_data(city)
        
        if df is not None:
            all_data[city] = df.to_dict(orient='records')
        else:
            all_data[city] = None

    return all_data


# function to get single city data
def get_single_city_data(city_name):
    df = city_data(city_name)

    if df is None:
        return None
    
    return df.to_dict(orient='records')


#----------------- GRAPH THING --------------------------


import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def generate_city_graph(city):
    df = city_data(city)

    if df is None or df.empty:
        return None

    PM10 = df['PM 10'].tolist()
    PM2_5 = df['PM 2.5'].tolist()
    aqi = df['AQI Value'].tolist()
    ozone = df['Ozone'].tolist()

    x = np.arange(1, len(aqi) + 1)

    # ---------- FIT + PREDICT -----------------
    poly1 = np.poly1d(np.polyfit(x, PM10, 2))
    poly2 = np.poly1d(np.polyfit(x, PM2_5, 2))
    poly3 = np.poly1d(np.polyfit(x, aqi, 2))
    poly4 = np.poly1d(np.polyfit(x, ozone, 2))

    future_x = np.arange(len(aqi)+1, len(aqi)+4)

    PM10_pred = poly1(future_x)
    PM2_5_pred = poly2(future_x)
    aqi_pred = poly3(future_x)
    ozone_pred = poly4(future_x)

    # ---------- PLOT ----------
    fig, axs = plt.subplots(2, 2, figsize=(10,8))
    fig.suptitle(city)

    # PM10
    axs[0,0].plot(x, PM10, marker='.', linestyle='solid', color='blue')
    axs[0,0].plot([x[-1]] + list(future_x),
                  [PM10[-1]] + list(PM10_pred),
                  linestyle='dashed', marker='.', color='red')
    axs[0,0].set_title("PM10")
    axs[0,0].grid(True)

    # PM2.5
    axs[0,1].plot(x, PM2_5, marker='.', linestyle='solid', color='violet')
    axs[0,1].plot([x[-1]] + list(future_x),
                  [PM2_5[-1]] + list(PM2_5_pred),
                  linestyle='dashed', marker='.', color='orange')
    axs[0,1].set_title("PM2.5")
    axs[0,1].grid(True)

    # AQI
    axs[1,0].plot(x, aqi, marker='.', linestyle='solid', color='red')
    axs[1,0].plot([x[-1]] + list(future_x),
                  [aqi[-1]] + list(aqi_pred),
                  linestyle='dashed', marker='.', color='blue')
    axs[1,0].set_title("AQI")
    axs[1,0].grid(True)

    # Ozone
    axs[1,1].plot(x, ozone, marker='.', linestyle='solid', color='green')
    axs[1,1].plot([x[-1]] + list(future_x),
                  [ozone[-1]] + list(ozone_pred),
                  linestyle='dashed', marker='.', color='violet')
    axs[1,1].set_title("Ozone")
    axs[1,1].grid(True)

    plt.tight_layout()

    # convert plot to image (important for Flask)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)

    # convert to base64 (easy for frontend)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64
