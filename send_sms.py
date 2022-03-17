import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

#Read flow info
# execution_context = client.studio \
#                   .v1 \
#                   .flows('FW2109518fbb6a0c790ad85b0506518ae3') \
#                   .executions('FNfae15ba7011ae2ffd537be8a9025cd54') \
#                   .execution_context() \
#                   .fetch()
    
# print(execution_context.context)

# Sends msg
# execution = client.studio \
#                   .v1 \
#                   .flows('FW2109518fbb6a0c790ad85b0506518ae3') \
#                   .executions \
#                   .create(to='+1', from_='+1')
    
# print(execution.sid)

# Sends body msg
message = client.messages.create(
    to="+1", 
    from_="+1",
    body="www.google.com")

print(message.sid)