#/usr/bin/env python
#from __future__ import absolute_import
from jira import JIRA
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# current date
#Date1 = os.popen("date +%Y/%m/%d")
#current_date1 = Date1.read()

# week before from current date
#Date2 = os.popen("date +%Y/%m/%d -d '-8 days'")
#week_before1 = Date2.read()

# Describe mail details
sender = 'devops-support@bazaarvoice.com'
receiver = ['balaji.k@bazaarvoice.com']
#CC = ['kelly.evans@bazaarvoice.com','balaji.partha@bazaarvoice.com']
msg = MIMEMultipart('alternative')
msg['Subject'] = "Blocked Tickets"
msg['From'] = sender
msg['To'] = ", ".join(receiver)


# authendicating jira with username & password
options = {
	'server':'https://bits.bazaarvoice.com/jira'
	 }
jira = JIRA(options, basic_auth=('btx','Theone@1'))

# DOS touched blocked tickets 
blocked_issues = jira.search_issues("labels = DOSTeam AND status = Blocked AND updated <= '-30d'", maxResults=5000)

#count of all blocked tickets
count_of_blocked_issues = len(blocked_issues)


# Create empty list[]
#tickets = []
#A = ""
# function to get the blocked tickets number
def list_of_tickets():
	A = ""	
	count = 0
	for i in blocked_issues:
		x = '<a href = "https://bits.bazaarvoice.com/jira/browse/%s">''%s</a>' % (i,i)
		count += 1
		A += x + ',' + '\t'
#		tickets.append(x)
#		ticket_list = [str(y) for y in tickets]
		if count == count_of_blocked_issues:	
#			return ticket_list
			return A


# HTML message template for mail
html = """\
<html>	
    <p>Hello Team,</p>
    <br></br>
    <p>Here is the list of blocked tickets</p>
    <p>Tickets not addressed for more than a 30 days</p>
    <p>No of tickets: %d</p> 
    <body>%s</body>
    <p>Please review these tickets and take necessary action</p>
    <br></br>
    <p>-DOS Team</p>
</html>""" % (count_of_blocked_issues,list_of_tickets())

#MIMEMultipart for mail
mail_body = MIMEText(html, 'html')
msg.attach(mail_body)


#Sending Mail
s = smtplib.SMTP('localhost')
s.sendmail(sender, receiver, msg.as_string())
s.quit()
