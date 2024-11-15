import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to, cc, bcc, subject, body):
    email_address = "akshithayadavbathula27@gmail.com"  # Your Gmail address
    app_password = "jrlp wumt ludt nimp"  # Your generated app password

    # Create the message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to
    msg['Cc'] = cc
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Combine all recipients (To, Cc, Bcc)
    recipients = [to] + cc.split(',') + bcc.split(',')

    # Connect to Gmail's SMTP server
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(email_address, app_password)  # Log in with your Gmail credentials (email + app password)
            server.sendmail(email_address, recipients, msg.as_string())  # Send the email

        # Log status to database
        status = "Sent"
        for recipient in recipients:
            cursor.execute("INSERT INTO email_status (recipient, subject, status, sent_time) VALUES (%s, %s, %s, NOW())", 
                           (recipient, subject, status))
        db.commit()
        
        print("Email Sent Successfully!")
        return "Email Sent Successfully!"
    
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"Failed to send email: {str(e)}"
