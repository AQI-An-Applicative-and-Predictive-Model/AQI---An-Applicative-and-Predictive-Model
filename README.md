 # AQI Predictor
**AQI and Applicative & Predictive Model**

Capstone Project | Group 188 | IIT Patna | CSDA 2nd Semester

**Live Demo**: 

## Problem Statement
Air pollution is India's silent health crisis with no future visibility in existing apps.

**# Key Issues:**
1. No Future Visibility: Apps show only current AQI, no tomorrow forecast
2. No Proactive Alerts: Users discover dangerous AQI after health damage  
3. Complex Data: Govt CPCB portals too technical for common users
4. Health Emergency: 1.67M deaths yearly need tech solutions urgently

## Our Solution
Web application that monitors current AQI and predicts next 3 days using Machine Learning.

**Key Features:**
1. **Live Dashboard**: Real-time AQI for 20 Indian cities with color codes
2. **3-Day ML Forecast**: Polynomial Regression predicts future pollution trends
3. **Email Alerts**: Auto warnings when AQI crosses 200 danger level
4. **Calendar Heatmap**: Monthly AQI view with CPCB official colors
5. **Pollutant Data**: Live PM2.5, PM10, Ozone values with health tips
6. **Responsive Design**: Works on mobile, tablet, desktop

## Tech Stack
**Frontend**: HTML5, CSS3, JavaScript, Chart.js  
**Backend**: Python, Flask, Pandas  
**ML**: NumPy Polynomial Regression, Matplotlib  
**Tools**: VS Code, GitHub, Render

## System Architecture
User → Frontend → Flask → Python Backend → CSV + ML Model

**3 Layers**: Presentation Layer, Application Layer, Data + ML Layer

## ML Model Working
**Algorithm**: Polynomial Regression Degree-2: y = ax² + bx + c

**Steps**:
1. Load last 30 days AQI from city CSV
2. Fit curve using `np.polyfit()` function
3. Predict next 3 days values
4. Plot actual data solid line, prediction dashed line

## Team Contribution

| **Name** | **Role** | **Work Done** |
| --- | --- | --- |
| **Ishan Vardan** | Frontend Lead | Complete UI/UX design, HTML, CSS, JavaScript, Responsive layouts, Chart.js graphs, Calendar heatmap, AQI color logic |
| **Yash** | Backend & ML Lead | CSV data management, Pandas data cleaning, NumPy ML model, Polynomial Regression, Matplotlib graph generation, 3-day forecasting |
| **Vaishnavi** | Integration Lead | Flask application, URL routing, Template rendering, Backend-ML integration, SMTP email alert system, Error handling |

## Future Scope
1. Integrate live CPCB API for real-time data
2. Upgrade to LSTM models for 7-day forecast
3. Build React Native mobile app
4. Add multi-city comparison feature

## 📊 Results & Output Screenshots

System tested successfully on multiple Indian cities. Screenshots below show actual working output.

### Screenshot 1: Homepage - City Selection
<img width="1600" height="763" alt="WhatsApp Image 2026-05-04 at 2 40 33 PM (3)" src="https://github.com/user-attachments/assets/e78eaf97-2c25-43cd-b990-7dbc2fb56de6" />

**Description**: Clean dark theme interface with search bar and 20 city cards. User can select any city to view live AQI data.

### Screenshot 2: Live Dashboard - New Delhi  
<img width="1600" height="769" alt="WhatsApp Image 2026-05-04 at 2 40 33 PM (2)" src="https://github.com/user-attachments/assets/58e8c4f1-7967-4c0e-b450-eff0178adb19" />

**Description**: Real-time dashboard showing AQI 111 Moderate with Orange color. Displays PM10, PM2.5, Ozone values with health advisory. Date picker and email subscription visible.

### Screenshot 3: ML Prediction Graphs
<img width="1600" height="759" alt="WhatsApp Image 2026-05-09 at 8 59 09 AM" src="https://github.com/user-attachments/assets/bec33dfc-58c8-45b4-8aad-f70399efb5ba" />

**Description**: 30-day historical trends with 3-day future forecast. Solid lines = actual data, Dashed lines = ML prediction for PM10, PM2.5. Model captures non-linear patterns.

### Screenshot 4: Calendar Heatmap - Mumbai
<img width="1600" height="762" alt="WhatsApp Image 2026-05-04 at 2 40 35 PM (1)" src="https://github.com/user-attachments/assets/569c2826-5dff-40a7-877d-2f149f883eeb" />

**Description**: May 2026 monthly AQI view using CPCB official colors. Each day color-coded: Green to Maroon. Helps users plan travel on safer days. Proves multi-city support.

### Screenshot 5: Email Alert System
<img width="720" height="758" alt="WhatsApp Image 2026-05-08 at 6 36 09 PM (1)" src="https://github.com/user-attachments/assets/6544284d-742b-46b4-9014-e0630f2513c6" />

**Description**: Automated Gmail alert triggered when AQI > 200. Contains city name, current AQI, health category, precautions, and dashboard link. System fully operational.

**Key Result Summary:**
- ✅ Delhi Dashboard: AQI 111 working with live data
- ✅ ML Forecast: 3-day prediction tested and accurate
- ✅ Mumbai Calendar: Multi-city scalability proven
- ✅ Email Alerts: Automated system functional for AQI > 200

---

**Project Status**: Completed and tested | **Built for cleaner air and healthier lives**
