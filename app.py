from flask import Flask, request, render_template
from data_loader import get_single_city_data
from graphs import generate_city_graph, get_health_advice, generate_aqi_calendar, predict_future_aqi, send_aqi_alert
from datetime import datetime
import calendar
import pandas as pd 
import os

app = Flask(__name__)


API_KEY = "YOUR_OPENWEATHER_API_KEY"


# -HOME -
@app.route("/")
def home():
    return render_template("index.html")

# - RESULT PAGE -


@app.route('/result')
def result():
    city = request.args.get('city')
    date = request.args.get('date')
    email = request.args.get('email')

    csv_path = f"Cities/{city}_final.csv"
    if not os.path.exists(csv_path):
        return "City data not found", 404

    full_df = pd.read_csv(csv_path)
    full_df['Date'] = pd.to_datetime(full_df['Date'])
    full_df = full_df.sort_values('Date')
    last_date = full_df['Date'].max()
    first_date = full_df['Date'].min()

    selected_date = None
    is_predicted = False

    if date:
        selected_date = pd.to_datetime(date)

        if selected_date > last_date:
        
            days_ahead = (selected_date - last_date).days
            if days_ahead > 3: 
                return render_template('result.html',
                    error="Predictions only available up to 3 days ahead",
                    city=city, selected_date=selected_date)

            data = predict_future_aqi(full_df, days_ahead, selected_date)
            is_predicted = True

        elif selected_date < first_date:
    
            return render_template('result.html',
                error=f"No data available before {first_date.strftime('%d %b %Y')}",
                city=city, selected_date=selected_date)
        else:
    
            match = full_df[full_df['Date'] == selected_date]
            if not match.empty:
                data = match.iloc[0].to_dict()
            else:
                # Date in range but missing - interpolate or show error
                return render_template('result.html',
                    error=f"No data recorded for {selected_date.strftime('%d %b %Y')}",
                    city=city, selected_date=selected_date)
    else:
        # No date - use latest
        data = full_df.iloc[-1].to_dict()
        selected_date = data['Date']

    if data is None:
        return "No data found", 404

    year = selected_date.year
    month = selected_date.month
    cal_data = generate_aqi_calendar(city, year, month)
    month_name = calendar.month_name[month]
    graph = generate_city_graph(city)
    health_advice = get_health_advice(data['AQI Value'])

    alert_sent = False
    if email and data:
        alert_sent = send_aqi_alert(email, city, data['AQI Value'], health_advice['level'])

    selected_display_data = selected_date.strftime('%d %b %Y')

    return render_template('result.html',
                         data=data,
                         graph=graph,
                         health_advice=health_advice,
                         is_red_alert = int(float(data['AQI Value'])) > 200,
                         city=city,
                         display_data=selected_display_data,
                         calendar=cal_data,
                         month_name=month_name,
                         year=year,
                         is_predicted=is_predicted,
                         selected_date=selected_date)


# - AQI API -
@app.route("/aqi")
def aqi():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City required"}), 400

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo = requests.get(geo_url).json()

    if not geo:
        return jsonify({"error": "City not found"}), 400

    lat, lon = geo[0]['lat'], geo[0]['lon']

    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(aqi_url).json()

    aqi = data['list'][0]['main']['aqi'] * 50
    pm25 = data['list'][0]['components']['pm2_5']
    pm10 = data['list'][0]['components']['pm10']
    ozone = data['list'][0]['components'].get('o3', 0)
    return jsonify({
        "city": city,
        "aqi": aqi,
        "pm25": pm25,
        "pm10": pm10,
        "ozone": ozone
    })

# - CSV GRAPH -
@app.route("/graph/<city>")
def graph(city):
    img = generate_city_graph(city)
    return jsonify({"image": img})

# - RUN -
if __name__ == "__main__":
    app.run(debug=True)
