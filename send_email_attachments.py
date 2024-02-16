import os
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

# Define email sender and receiver
email_sender = 'justinguuuu@gmail.com'  # Replace 'Your email' with the sender's email address
email_password = os.environ.get("EMAIL_PASSWORD")  # Retrieve email password from environment variables
email_receiver = 'The email of the receiver'  # Replace 'The email of the receiver' with the recipient's email address

# Set the subject and body of the email
subject = 'This is the subject'  # Define the subject of the email
body = "This is the body of the email"  # Define the body of the email

em = EmailMessage()  # Create an instance of EmailMessage
em['From'] = email_sender  # Set the sender's email address
em['To'] = email_receiver  # Set the recipient's email address
em['Subject'] = subject  # Set the subject of the email
em.set_content(body)  # Set the content of the email

# Make the message multipart
em.add_alternative(body, subtype='html')  # Set the email content type to HTML

# Attach the image file
with open('Image.png', 'rb') as attachment_file:  # Open the image file in binary mode
    file_data = attachment_file.read()  # Read the contents of the image file
    file_name = attachment_file.name.split("/")[-1]  # Extract the filename from the file path

attachment = MIMEBase('application', 'octet-stream')  # Create a MIMEBase instance
attachment.set_payload(file_data)  # Set the payload of the attachment
encoders.encode_base64(attachment)  # Encode the attachment data in Base64 format
attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')  # Set the attachment filename
em.attach(attachment)  # Attach the file to the email message

# Add SSL (layer of security)
context = ssl.create_default_context()  # Create a default SSL context

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:  # Connect to Gmail's SMTP server over SSL
    smtp.login(email_sender, email_password)  # Log in to the SMTP server using the sender's email and password
    smtp.sendmail(email_sender, email_receiver, em.as_string())  # Send the email
