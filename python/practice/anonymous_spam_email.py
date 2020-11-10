#!/usr/bin/env python

# Note: Haven't checked but the script seems working
# Received a spam mail, it works 
# http://anonymouse.org/

import mechanize

br = mechanize.Browser()

to = raw_input("Enter the recipient address:  ")
subject = raw_input("Enter the subject: ")

print "Message: "
message = raw_input(">")


url = "http://anonymouse.org/anonemail.html"
headers  = "Mozila/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)"
br.headers = [('User-agent', headers)]

br.open(url)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(False)
br.set_debug_redirects(False)

br.select_form(nr=0)

br.form['to'] = to
br.form['subject'] = subject
br.form['text'] = message

result = br.submit()

response= br.response().read()

print response

if "The e-mail has been sent anonymously!" in response:
	print "The email has been sent successfully!! \n The recipient will get it in 12 hours!!"
else:
	print "failed to send email!!"




