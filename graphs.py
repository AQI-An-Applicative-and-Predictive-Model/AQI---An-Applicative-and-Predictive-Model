import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os
from numpy import polyfit, poly1d
import calendar
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_aqi_alert(to_email, city, aqi, level):
    print(f"DEBUG: Attempting to send email to {to_email}") 
    
    sender_email = "aqi.alert.notify@gmail.com"  
    sender_password = "orwucrszffxrizir"  
    
    if int(float(aqi)) <= 150:
        print("DEBUG: AQI <= 150, no email sent") 
        return False
    
    print(f"DEBUG: AQI is {aqi}, preparing email") 
    
    subject = f"🔴 AQI Alert: {city} is {level} - {int(float(aqi))}"
    
    body = f"""
    Red Alert for {city}
    
    Current AQI: {int(float(aqi))}
    Level: {level}
    
    Health Advice: Avoid outdoor activities. Keep windows closed. Wear N95 mask outside.
    
    Check dashboard: http://localhost:5000/result?city={city}
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"SUCCESS: Alert sent to {to_email}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to send: {e}") 
        return False
    
def check_red_alert(city, aqi_value, email_to=None):
    """
    Triggers alert if AQI > 200. Returns True if alert sent.
    """
    aqi = int(float(aqi_value))
    
    # Red alert threshold
    if aqi <= 200:
        return False
    
    # Determine level
    if aqi <= 300:
        level = "Very Unhealthy"
        color = "#8f3f97"
    else:
        level = "Hazardous"
        color = "#7e0023"
    
    # Send email if address provided
    if email_to:
        send_aqi_email(city, aqi, level, color, email_to)
    
    return True

def send_aqi_email(city, aqi, level, color, to_email):
    sender_email = "your_email@gmail.com"
    sender_password = "your_16_char_app_password"  # Generate from Google Account
    
    subject = f"🔴 RED ALERT: {city} AQI is {aqi} - {level}"
    
    html = f"""
    <html>
      <body style="font-family: Arial; text-align: center;">
        <div style="background: {color}; padding: 30px; border-radius: 15px; color: white;">
          <h1 style="font-size: 48px; margin: 0;">{aqi}</h1>
          <h2>{level}</h2>
          <p style="font-size: 18px;">Air Quality in {city}</p>
        </div>
        <div style="margin-top: 20px; color: #333;">
          <h3>Health Advisory:</h3>
          <p>Everyone should avoid outdoor activities. Keep windows closed.</p>
          <p>Wear N95 mask if you must go outside.</p>
        </div>
      </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Red alert email sent for {city} AQI {aqi}")
    except Exception as e:
        print(f"Email failed: {e}")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from io import BytesIO
import base64

# Use modern style
plt.style.use('seaborn-v0_8-whitegrid')

def generate_city_graph(city):
    csv_path = f"Cities/{city}_final.csv"
    
    if not os.path.exists(csv_path):
        return None
    
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').tail(30)
    
    if df.empty:
        return None
    
    # Extract data
    PM10 = df['PM10'].tolist()
    PM2_5 = df['PM2.5'].tolist()
    aqi = df['AQI Value'].tolist()
    ozone = df['Ozone'].tolist()
    dates = df['Date'].tolist()
    
    x = np.arange(1, len(aqi) + 1)
    
    #  AQI for prediction
    poly_aqi = np.poly1d(np.polyfit(x, aqi, 2))
    x_pred = np.arange(1, len(aqi) + 4)
    future_dates = pd.date_range(start=dates[-1], periods=4, freq='D')[1:]
    
    # Create figure with better proportions
    fig, ax = plt.subplots(figsize=(14, 6), facecolor='white')
    
    # AQI bands first 
    ax.axhspan(0, 50, facecolor='#10b981', alpha=0.08, zorder=0)
    ax.axhspan(50, 100, facecolor='#fbbf24', alpha=0.08, zorder=0)
    ax.axhspan(100, 150, facecolor='#f97316', alpha=0.08, zorder=0)
    ax.axhspan(150, 200, facecolor='#ef4444', alpha=0.08, zorder=0)
    ax.axhspan(200, 300, facecolor='#a855f7', alpha=0.08, zorder=0)
    
    # Plot main lines 
    ax.plot(dates, PM10, label='PM10', color='#f97316', linewidth=2, alpha=0.8)
    ax.plot(dates, PM2_5, label='PM2.5', color='#dc2626', linewidth=2, alpha=0.8)
    ax.plot(dates, aqi, label='AQI', color='#111827', linewidth=3, zorder=5)
    ax.plot(dates, ozone, label='Ozone', color='#059669', linewidth=2, alpha=0.8)
    
    # AQI prediction 
    all_dates = dates + list(future_dates)
    ax.plot(all_dates, poly_aqi(x_pred), label='AQI 5-Day Forecast', 
            color='#111827', linestyle='--', linewidth=2.5, alpha=0.5)
    
    # Formatting
    ax.set_xlabel('Date', fontsize=13, fontweight='600')
    ax.set_ylabel('Concentration / AQI Value', fontsize=13, fontweight='600')
    ax.set_title(f'{city} - Air Quality Trends', fontsize=16, fontweight='700', pad=20)
    

    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    

    ax.legend(loc='upper left', fontsize=11, framealpha=0.9, edgecolor='none')
    
    # Cap Y-axis 
    y_max = max(max(aqi[:-1]), max(PM10), max(PM2_5)) * 1.15 
    ax.set_ylim(0, min(y_max, 300))
    
    # Cleaner date format
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3)) 
    plt.xticks(rotation=0, ha='center')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#d1d5db')
    ax.spines['bottom'].set_color('#d1d5db')
    
    plt.tight_layout()
    
    # Convert to base64
    img = BytesIO()
    plt.savefig(img, format='png', dpi=120, bbox_inches='tight', facecolor='white')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return plot_url

def get_health_advice(aqi):
    aqi = int(float(aqi))
    
    if aqi <= 50:
        return {"level": "Good", "text": "Air quality is satisfactory, and air pollution poses little or no risk.", "color": "green"}
    elif aqi <= 100:
        return {"level": "Moderate", "text": "Air quality is acceptable. However, there may be a risk for some people.", "color": "yellow"}
    elif aqi <= 150:
        return {"level": "Unhealthy for Sensitive Groups", "text": "Members of sensitive groups may experience health effects. General public is less likely to be affected.", "color": "orange"}
    elif aqi <= 200:
        return {"level": "Unhealthy", "text": "Some members of the general public may experience health effects; members of sensitive groups may experience more serious effects.", "color": "red"}
    elif aqi <= 300:
        return {"level": "Very Unhealthy", "text": "Health alert: The risk of health effects is increased for everyone.", "color": "purple"}
    else:
        return {"level": "Hazardous", "text": "Health warning of emergency conditions: everyone is more likely to be affected.", "color": "maroon"}


def generate_aqi_calendar(city, year, month):
    file_path = os.path.join('Cities', f'{city}_final.csv')
    if not os.path.exists(file_path):
        return {}

    df = pd.read_csv(
        file_path,
        names=['Date','PM10','PM2.5','AQI Value','Ozone'],
        header=None,
        usecols=[0,1,2,3,4]
    )

    df[['AQI Value']] = df[['AQI Value']].apply(pd.to_numeric, errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Filter for specific month/year
    df_month = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]

    # If multiple readings per day, take the last one
    df_daily = df_month.groupby(df_month['Date'].dt.date)['AQI Value'].last().to_dict()

    # Add color based on AQI
    calendar_data = {}
    for date, aqi in df_daily.items():
        if aqi <= 50:
            color = '#00e400' # Green - Good
        elif aqi <= 100:
            color = '#ffff00' # Yellow - Moderate
        elif aqi <= 150:
            color = '#ff7e00' # Orange - Unhealthy for Sensitive
        elif aqi <= 200:
            color = '#ff0000' # Red - Unhealthy
        elif aqi <= 300:
            color = '#8f3f97' # Purple - Very Unhealthy
        else:
            color = '#7e0023' # Maroon - Hazardous

        calendar_data[date.day] = {'aqi': int(aqi), 'color': color}

    return calendar_data



import numpy as np

def predict_future_aqi(df, days_ahead, target_date):
    """Predict AQI values for N days ahead using polynomial fit"""

    PM10 = df['PM 10'].dropna().tolist()
    PM2_5 = df['PM 2.5'].dropna().tolist()
    aqi = df['AQI Value'].dropna().tolist()
    ozone = df['Ozone'].dropna().tolist()

    x = np.arange(1, len(aqi) + 1)

    # Fit 2nd degree polynomials
    poly_pm10 = np.poly1d(np.polyfit(x, PM10, 2))
    poly_pm25 = np.poly1d(np.polyfit(x, PM2_5, 2))
    poly_aqi = np.poly1d(np.polyfit(x, aqi, 2))
    poly_ozone = np.poly1d(np.polyfit(x, ozone, 2))

    # Predict for future day
    future_x = len(aqi) + days_ahead

    # Clamp predictions to reasonable ranges
    pred_pm10 = max(0, round(poly_pm10(future_x), 1))
    pred_pm25 = max(0, round(poly_pm25(future_x), 1))
    pred_aqi = max(0, min(500, round(poly_aqi(future_x), 0))) # AQI 0-500
    pred_ozone = max(0, round(poly_ozone(future_x), 1))

    return {
        'Date': target_date,
        'City': df['City'].iloc[0] if 'City' in df.columns else 'Unknown',
        'PM 10': pred_pm10,
        'PM 2.5': pred_pm25,
        'AQI Value': pred_aqi,
        'Ozone': pred_ozone
    }
