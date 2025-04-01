import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "bionano.rajdus@gmail.com"
receiver_email = "bionano.rajdus@gmail.com"
password = "qqsx niru xtzm tyru"

report_str = ""

def add_to_email(text : str) -> None:
    global report_str
    report_str += text
    
def change_email(text : str) -> None:
    global report_str
    report_str = text
    
def send_email(body : str, subject : str = None) -> None:
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    if subject is not None:
        msg["Subject"] = subject
    else:
        msg["Subject"] = "Bionano report"

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        
def send_report():
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Bionano report"

    msg.attach(MIMEText(report_str, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")