import utils.log_tracking as log 

import smtplib
from email.message import EmailMessage

def send_message(sendTo: str, subject: str, bodyText: str):

    #Database connections parameters
    SMTP_SERVER = 'smtp.office365.com'
    SMTP_PORT = 587
    EMAIL_SENDER = 'payrollreports@payrollsolutions.cc'
    EMAIL_PASSWORD = '6a3233bA42?'

    msg = EmailMessage()
    msg.set_content(bodyText)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = sendTo

    try:
        with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER,EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        log.write_log(e,'error')



