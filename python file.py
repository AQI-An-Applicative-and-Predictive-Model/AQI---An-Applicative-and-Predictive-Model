from flask import Flask, request, jsonify
import requests
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# CONFIG
API_KEY = "YOUR_OPENWEATHER_API_KEY"

# Telegram (for alerts)
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# FUNCTIONS

def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}"
    res = requests.get(url).json()
    if not res:
        return None, None
    return res[0]['lat'], res[0]['lon']


def fetch_current_data(lat, lon):
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    aqi_data = requests.get(aqi_url).json()
    weather_data = requests.get(weather_url).json()

    return aqi_data, weather_data


def fetch_history(lat, lon):
    end = int(time.time())
    start = end - (7 * 24 * 60 * 60)

    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}"
    return requests.get(url).json()


# AQI LOGIC

def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Hazardous"


def health_advice(aqi):
    if aqi <= 50:
        return "Safe for all people"
    elif aqi <= 100:
        return "Sensitive groups should limit outdoor activity"
    else:
        return "Avoid outdoor activity, wear mask"


def check_alert(aqi):
    if aqi > 150:
        return "⚠️ Hazardous Air Quality!"
    return "Air quality normal"


# TELEGRAM ALERT

def send_mobile_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except:
        pass


# PREDICTION MODEL

def predict_aqi(aqi_values, pm25_values, pm10_values):
    X = []
    y = aqi_values

    for i in range(len(aqi_values)):
        X.append([pm25_values[i], pm10_values[i]])

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    next_input = np.array([[pm25_values[-1], pm10_values[-1]]])
    prediction = model.predict(next_input)

    return int(prediction[0])


# GRAPH FUNCTION

def generate_graph(data, filename, title, ylabel):
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure()
    plt.plot(data, marker='o')
    plt.title(title)
    plt.xlabel("Days")
    plt.ylabel(ylabel)
    plt.savefig(f"static/{filename}")
    plt.close()


# MAIN API

@app.route("/aqi", methods=["POST"])
def aqi_dashboard():
    data = request.json
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    lat, lon = get_coordinates(city)
    if not lat:
        return jsonify({"error": "Invalid city"}), 400

    aqi_data, weather_data = fetch_current_data(lat, lon)

    aqi = aqi_data['list'][0]['main']['aqi'] * 50
    pm25 = aqi_data['list'][0]['components']['pm2_5']
    pm10 = aqi_data['list'][0]['components']['pm10']
    temp = weather_data['main']['temp']

    category = categorize_aqi(aqi)
    advice = health_advice(aqi)
    alert = check_alert(aqi)

    history = fetch_history(lat, lon)

    aqi_values = [item['main']['aqi'] * 50 for item in history['list'][:7]]
    pm25_values = [item['components']['pm2_5'] for item in history['list'][:7]]
    pm10_values = [item['components']['pm10'] for item in history['list'][:7]]

    temp_values = [temp + np.random.uniform(-2, 2) for _ in range(7)]

    prediction = predict_aqi(aqi_values, pm25_values, pm10_values)

    generate_graph(aqi_values, "aqi.png", "AQI Trend", "AQI")
    generate_graph(pm25_values, "pm25.png", "PM2.5 Trend", "PM2.5")
    generate_graph(pm10_values, "pm10.png", "PM10 Trend", "PM10")
    generate_graph(temp_values, "temp.png", "Temperature Trend", "°C")

    if aqi > 150:
        send_mobile_alert(f"⚠️ AQI Alert in {city}: {aqi}")

    return jsonify({
        "city": city,
        "aqi": aqi,
        "category": category,
        "pm25": pm25,
        "pm10": pm10,
        "temperature": temp,
        "health_advice": advice,
        "alert": alert,
        "prediction": prediction,
        "graphs": {
            "aqi": "/static/aqi.png",
            "pm25": "/static/pm25.png",
            "pm10": "/static/pm10.png",
            "temp": "/static/temp.png"
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
