### Write code for the new module here and import it from agent.py.import os
import requests
import os

# Retrieve environment variables using the .get method
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SENDER = os.environ.get("TWILIO_SENDER")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")

# Define the URL for the Twilio API
url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

async def send_whatsapp_message(message):
    """
    Sends a WhatsApp message using the Twilio API.

    Args:
        message (str): The message to be sent.

    Returns:
        dict: The response from the Twilio API.
    """
    try:
       
        data = {
            "From": f"whatsapp:+{TWILIO_SENDER}",
            "Body": message,
            "To": f"whatsapp:+91{PHONE_NUMBER}"
        }

        # Make the POST request to the Twilio API
        response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

        # Return the JSON response from the server
        return response.json()
    except Exception as e:
        # Return an error message in case of failure
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    message = "Hello testing!"
    response = send_whatsapp_message(message)
    print(response)
