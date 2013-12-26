import os
import config
import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/%s/messages" % config.MAILGUN_DOMAIN,
        auth=("api", config.MAILGUN_API_KEY),
        data={"from": "Excited User <me@wanderingstan.mailgun.org>",
              "to": ["stan@wanderingstan.com", "wanderingstan@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

print "Does this appear?"
print ( send_simple_message())
