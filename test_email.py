import smtplib
from email.mime.text import MIMEText

sender_email = "aqi.alert.notify@gmail.com"  
sender_password = "orwucrszffxrizir"  
to_email = "vaishnavikadam1985@gmail.com"

msg = MIMEText("Test from AQI project")
msg['Subject'] = "Test Email"
msg['From'] = sender_email
msg['To'] = to_email

try:
    print("Connecting to Gmail...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("Logging in...")
    server.login(sender_email, sender_password)
    print("Sending...")
    server.send_message(msg)
    server.quit()
    print("SUCCESS: Email sent. Check inbox + spam.")
except Exception as e:
    print(f"FAILED: {e}")
