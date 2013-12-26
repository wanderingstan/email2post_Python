# -*- coding: utf-8 -*-

# cgi handler that is called by mailgun when a new email is received

# Test with: http://email2post.wanderingstan.com/test.html

import cgi, cgitb
from e2p_config import config

import pprint
pp = pprint.PrettyPrinter(indent=4)

cgitb.enable()

form = cgi.FieldStorage()

#
# Save the email
#
from time import gmtime, strftime

datetime = strftime("%Y-%m-%dT%H-%M-%SZ", gmtime())
filename = "%s.txt" % (datetime) # e.g. 2014-06-06T12-05-30Z_joe

f = open(os.path.join(config['FILE_STORAGE_PATH'],filename), 'w')
if 'body-plain' in form:
    f.write(form['body-plain'].value)
f.close()


#
# Get attached file
#
if 'userfile' in form:
    fileitem=form['userfile']
    if fileitem.file:
        #yay...we got a file
        attachedfile=fileitem.file.read()

message = ('\n\n\n\n\n\nGot a message for mailbox %s.\n' % form['mailbox'].value)
# message += pp.pformat(form)

if 'To' in form:
    message += "\nTo:\n" + form['To'].value
if 'From' in form:
    message += "\nfrom:\n" + form['From'].value
if 'Date' in form:
    message += "\ndate:\n" + form['Date'].value
if 'Subject' in form:
    message += "\nsubject:\n" + form['Subject'].value
if 'body-plain' in form:
    message += "\nbody-plain:\n" + form['body-plain'].value
if 'stripped-html' in form:
    message += "\nstripped-html:\n" + form['stripped-html'].value

print """\
Content-Type: text/html\n
<html><body>
<pre>%s</pre>
</body></html>
""" % (message,)

# Debug log
f = open(os.path.join(config['FILE_STORAGE_PATH'],'email.log'), 'a')
if 'mailbox' in form:
    f.write(message)
f.close()

