import csv
import pandas as pd
from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = 'ACeed438662a937f039272a41792869278'
auth_token = '6978ad85367c11ba8947946e9d57c017'
print("got the hardcoded token")
# Initialize Twilio client
client = Client(account_sid, auth_token)
print("client made")
# Open the CSV file and read the contacts
with open('contacts.csv', 'r') as file:
    reader = csv.reader(file)
    #next(reader) # Skip header row
    for name, phone_number in reader:
        # Send a text message to the phone number
        message = client.messages.create(
            body='Hello World',
            from_='+18559554043',
            to=phone_number
        )
        print(f"Message sent to {name} ({phone_number}): {message.sid}")