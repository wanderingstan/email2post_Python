import os
from flask import Flask
from flask import request
import config
import pprint

# Running on Hostgator?
# https://groups.google.com/d/msg/django-users/DVvnqb7iVVI/Xcko-awlBGMJ

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/email')
def email():
    print "Does this appear?"
    print ( send_simple_message())
    return "done"

@app.route('/recieve_email',methods=['GET', 'POST'])
def receive_email():
    return pp.pformat(flask.request)

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/samples.mailgun.org/messages",
        auth=("api", config.MAILGUN_API_KEY),
        data={"from": "Excited User <me@samples.mailgun.org>",
              "to": ["stan@wanderingstan.com", "wanderingstan@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})
