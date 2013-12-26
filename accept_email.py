# -*- coding: utf-8 -*-

# cgi handler that is called by mailgun when a new email is received

# Test with: http://email2post.wanderingstan.com/test.html

import cgi, cgitb
from e2p_config import config

import pprint
pp = pprint.PrettyPrinter(indent=4)

cgitb.enable()

form = cgi.FieldStorage()

message=""

# get the fileitem
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

# body-plain
#
f = open('email.log', 'a')
if 'mailbox' in form:
    f.write(message)
f.close()