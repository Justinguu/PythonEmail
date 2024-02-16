import os
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

# Define email sender
email_sender = 'Your email'  # Replace 'Your email' with the sender's email address
email_password = os.environ.get("EMAIL_PASSWORD")  # Retrieve email password from environment variables

# Set the subject and body of the email
subject = 'Check out my new video!'  # Define the subject of the email
body = "I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg"  # Define the body of the email

# Reading the CSV file
csv_path = 'multiple_emails.csv'  # Path to the CSV file containing email addresses and attachment filenames
emails_df = pd.read_csv(csv_path)  # Read the CSV file into a pandas DataFrame

# Looping through the CSV file and sending emails with attachments
for index, row in emails_df.iterrows():  # Iterate through each row of the DataFrame
    email_receiver = row['Receiver']  # Get the email address of the receiver from the current row
    attachment_file_name = row['Attachment']  # Get the filename of the attachment from the current row

    # Define email parameters
    em = EmailMessage()  # Create an instance of EmailMessage
    em['From'] = email_sender  # Set the sender's email address
    em['To'] = email_receiver  # Set the recipient's email address
    em['Subject'] = subject  # Set the subject of the email
    em.set_content(body)  # Set the content of the email

    # Make the message multipart
    em.add_alternative(body, subtype='html')  # Set the email content type to HTML

    # Attach the file
    with open(attachment_file_name, 'rb') as attachment_file:  # Open the attachment file in binary mode
        file_data = attachment_file.read()  # Read the contents of the attachment file
        file_name = os.path.basename(attachment_file_name)  # Extract the filename from the attachment file path

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
