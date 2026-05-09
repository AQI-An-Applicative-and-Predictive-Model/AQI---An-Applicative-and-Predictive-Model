import pandas as pd
import os

def get_single_city_data(city, date=None):
    file_path = os.path.join('Cities', f'{city}_final.csv')
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(
    file_path,
    names=['Date','PM10','PM2.5','AQI Value','Ozone'], 
    header=None,
    usecols=[0,1,2,3,4] 
)
    
    df[['PM10','PM2.5','AQI Value','Ozone']] = df[['PM10','PM2.5','AQI Value','Ozone']].apply(pd.to_numeric, errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.sort_values('Date')

    if date:
        date = pd.to_datetime(date).date()
        result = df[df['Date'].dt.date == date]
    else:
        result = df.tail(1)

    if result.empty:
        return None
    return result.iloc[-1].to_dict()
