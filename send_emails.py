import os
import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'Your email'  # Replace 'Your email' with the sender's email address
email_password = os.environ.get("EMAIL_PASSWORD")  # Retrieve email password from environment variables
email_receiver = 'The email of the receiver'  # Replace 'The email of the receiver' with the recipient's email address

# Set the subject and body of the email
subject = 'Check out my new video!'  # Define the subject of the email
body = """
I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
"""  # Define the body of the email

em = EmailMessage()  # Create an instance of EmailMessage
em['From'] = email_sender  # Set the sender's email address
em['To'] = email_receiver  # Set the recipient's email address
em['Subject'] = subject  # Set the subject of the email
em.set_content(body)  # Set the content of the email

# Add SSL (layer of security)
context = ssl.create_default_context()  # Create a default SSL context

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:  # Connect to Gmail's SMTP server over SSL
    smtp.login(email_sender, email_password)  # Log in to the SMTP server using the sender's email and password
    smtp.sendmail(email_sender, email_receiver, em.as_string())  # Send the email
