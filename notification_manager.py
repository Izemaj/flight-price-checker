from twilio.rest import Client

TWILIO_ACCOUNT_SID = "ACef072d187edafbc1d29732de8f2eb486"
TWILIO_AUTH_TOKEN = "e5e285f0e35cbe2471204a3130b1e535"
TWILIO_PHONE_NUMBER = "+15077065463"
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to="+2349166914896"
        )
        print(message.status)