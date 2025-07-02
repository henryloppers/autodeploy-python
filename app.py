import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage

def generate_report():
    # Generate fake data
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    data = {
        'Date': np.random.choice(dates, 100),
        'Sales': np.random.randint(100, 1000, size=100)
    }
    df = pd.DataFrame(data)

    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    summary = df.groupby('Month')['Sales'].sum().reset_index()

    report_file = 'monthly_report.xlsx'
    summary.to_excel(report_file, index=False)
    print(f"✅ Report generated: {report_file}")
    return report_file

def send_email_report(file_path):
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    RECIPIENT = os.getenv('EMAIL_RECIPIENT')

    msg = EmailMessage()
    msg['Subject'] = 'Automated Daily Excel Report'
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT

    msg.set_content('Hi,\n\nPlease find the attached daily Excel sales report.\n\nBest regards,\nAutomation Bot')

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = file_path

    msg.add_attachment(file_data, maintype='application',
                       subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                       filename=file_name)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print(f"✅ Email sent to {RECIPIENT} with attachment {file_name}")

if __name__ == '__main__':
    report_file = generate_report()
    send_email_report(report_file)
