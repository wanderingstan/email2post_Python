# -*- coding: utf-8 -*-

# Get email from a POP email server
#
# http://stackoverflow.com/questions/8307809/save-email-attachment-python3-pop3-ssl-gmail
# http://stackoverflow.com/questions/1225586/checking-email-with-python
# https://www.google.com/search?q=python+pop+email+example&oq=python+pop+email+&aqs=chrome.1.69i57j0l5.5867j0j1&sourceid=chrome&espv=210&es_sm=119&ie=UTF-8

import poplib
import email
import os

from e2p_config import config

class getEmail(object):
    def __init__(self):
        self.savedir="/tmp"

    def save_email(self):

        self.connection = poplib.POP3_SSL(config['POP_EMAIL_SERVER'], 995)
        self.connection.set_debuglevel(1)
        self.connection.user(config['POP_EMAIL_ACCOUNT'])
        self.connection.pass_(config['POP_EMAIL_PASS'])

        emails, total_bytes = self.connection.stat()
        print("{0} emails in the inbox, {1} bytes total".format(emails, total_bytes))
        # return in format: (response, ['mesg_num octets', ...], octets)
        msg_list = self.connection.list()
        print(msg_list)

        # messages processing
        for i in range(emails):

            # return in format: (response, ['line', ...], octets)
            response = self.connection.retr(i+1)

            raw_message = response[1]

            print raw_message
            # str_message = email.message_from_bytes(b'\n'.join(raw_message)) #python 3
            str_message = email.message_from_string("\n".join(raw_message))

            sender = str_message['From']
            subject = str_message['Subject']
            print ("Sender is %s" % sender)

            # save attach
            for part in str_message.walk():
                print(part.get_content_type())

                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get('Content-Disposition') is None:
                    print("no content dispo")
                    continue

                filename = part.get_filename()
                if not(filename): filename = "test.txt"
                print(filename)

                print ("Saving to %s" % os.path.join(self.savedir, filename))
                fp = open(os.path.join(self.savedir, filename), 'wb')
                fp.write(part.get_payload(decode=1))
                fp.close

            # # delete it
            # self.connection.dele(i+1)
            # print ("Deleted email %s" % (i+1))

        self.connection.quit()

        #I  exit here instead of pop3lib quit to make sure the message doesn't get removed in gmail
        # import sys
        # sys.exit(0)

d=getEmail()
d.save_email()
