from email.mime.text import MIMEText
from typing import Optional
import smtplib

class SendEmailVerify:
    @staticmethod
 
    def sendVerify(token:str ): #(token: str, to_email: str):
        
        # create email
        email_address = "ditiran10@gmail.com" # type Email
        email_password = "wicf zxtl auhi vitj" # If you do not have a gmail apps password, create a new app with using generate password. Check your apps and passwords https://myaccount.google.com/apppasswords
        
        verification_url = f"http://localhost:8000/user/verify/{token}"
        subject = "Activate your account"
        body = f"Please click on the link to verify your email and activate your account: {verification_url}"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = "ditiran10@gmail.com" # to_email we want to check the email
       
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)