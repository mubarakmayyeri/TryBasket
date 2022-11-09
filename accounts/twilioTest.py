# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from django.conf import settings

# Find your Account SID and Auth Token in Account Info and set the environment variables.
# See http://twil.io/secure
account_sid =settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
client = Client(account_sid, auth_token)

def verify():
  message = client.messages.create(
  body='Hi there',
  from_='+12059734341',
  to='+917012556289'
 )

  print(message.sid)