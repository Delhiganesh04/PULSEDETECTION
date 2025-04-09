import serial
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Serial Communication Setup
SERIAL_PORT = "COM6"  # Change to the correct port (e.g., "/dev/ttyUSB0" for Linux/Mac)
BAUD_RATE = 115200

# Email Credentials
SMTP_SERVER = "mail.datareef.co.in"
SMTP_PORT = 465
EMAIL_ADDRESS = "alert@datareef.co.in"
EMAIL_PASSWORD = "liveinlab@"  # Replace with actual password
TO_EMAIL = "delhiiganesh29@gmail.com"

# Function to send email alert
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to listen for serial data and send alerts
def listen_serial():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow connection to establish

    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                print("Received:", line)

                if "ALERT" in line:
                    subject = "⚠ Heart Rate Alert!"
                    body = f"Warning! Abnormal heart rate detected. Check the patient immediately.\n\nDetails:\n{line}"
                    send_email(subject, body)
        except KeyboardInterrupt:
            print("\nSerial communication stopped.")
            ser.close()
            break
        except Exception as e:
            print(f"Error: {e}")

# Run the listener
if __name__ == "__main__":
    print("Listening for serial data...")
    listen_serial()
