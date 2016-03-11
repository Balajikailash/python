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

# 2 weeks before from current date
#Date3 = os.popen("date +%Y/%m/%d -d '-15 days'")
#week_before2 = Date3.read()

# 3 weeks before from current date
#Date4 = os.popen("date +%Y/%m/%d -d '-22 dayes'")
#week_before3 = Date3.read()


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
blocked_issues_for_1week = jira.search_issues("labels = DOSTeam AND status = Blocked AND updated < '-7d' ORDER BY updated DESC", maxResults=5000)
blocked_issues_for_2week = jira.search_issues("labels = DOSTeam AND status = Blocked AND updated < '-14d' ORDER BY updated DESC", maxResults=5000)
blocked_issues_for_3week = jira.search_issues("labels = DOSTeam AND status = Blocked AND updated < '-21d' ORDER BY updated DESC", maxResults=5000)
blocked_issues_for_4weekandmore = jira.search_issues("labels = DOSTeam AND status = Blocked AND updated < '-28d' ORDER BY updated DESC", maxResults=5000)

#count of all blocked tickets
count_of_blocked_issues_for_1week = len(blocked_issues_for_1week)
count_of_blocked_issues_for_2week = len(blocked_issues_for_2week)
count_of_blocked_issues_for_3week = len(blocked_issues_for_3week)
count_of_blocked_issues_for_4weekandmore = len(blocked_issues_for_4weekandmore)


# Create empty list[]
#tickets = []
#A = ""
# function to get the blocked tickets number
def list_of_blocked_tickets_for_1week():
	A1 = ""	
	count = 0
	for i in blocked_issues_for_1week:
		x = '<a href = "https://bits.bazaarvoice.com/jira/browse/%s">''%s</a>' % (i,i)
		count += 1
		A1 += x + ',' + '\t'
#		tickets.append(x)
#		ticket_list = [str(y) for y in tickets]
		if count == count_of_blocked_issues_for_1week:	
#			return ticket_list
			return A1


def list_of_blocked_tickets_for_2week():
	A2 = ""
	count = 0
	for i in blocked_issues_for_2week:
		x = '<a href = "https://bits.bazaarvoice.com/jira/browse/%s">''%s</a>' % (i,i)
		count += 1
		A2 += x + ',' + '\t'
		if count == count_of_blocked_issues_for_2week:
			return A2

def list_of_blocked_tickets_for_3week():
	A3 = ""
	count = 0
	for i in blocked_issues_for_3week:
		x = '<a href = "https://bits.bazaarvoice.com/jira/browse/%s">''%s</a>' % (i,i)
		count += 1
		A3 += x + ',' + '\t'
		if count == count_of_blocked_issues_for_3week:
			return A3

def list_of_blocked_tickets_for_4weekandmore():
	A4 = ""
	count = 0
	for i in blocked_issues_for_4weekandmore:
		x = '<a href = "https://bits.bazaarvoice.com/jira/browse/%s">''%s</a>' % (i,i)
		count += 1
		A4 += x + ',' + '\t'
		if count == count_of_blocked_issues_for_4weekandmore:
			return A4
# HTML message template for mail
html = """\
<html>	
    <p>Hello Team,</p>
    <br></br>
    <p>Here is the list of blocked tickets</p>
    <p>Tickets are not addressed for more than a week</p>
    <p>No of tickets: %d</p> 
    <body>%s</body>
    <br></br>
    <p>Tickets are not addressed for more than 2 weeks</p>
    <p>No of tickets: %d</p>
    <body>%s</body>
    <br></br>
    <p>Tickets are not addressed for more than 3 weeks</p>
    <p>No of tickets: %d</p>
    <body>%s</body>
    <br></br>
    <p>Tickets are not addressed for more than 4 weeks</p>
    <p>No of tickets: %d</p>
    <body>%s</body>
    <br></br>
    <p>Please review these tickets and take necessary action</p>
    <br></br>
    <p>-DOS Team</p>
</html>""" % (count_of_blocked_issues_for_1week,list_of_blocked_tickets_for_1week(),count_of_blocked_issues_for_2week,list_of_blocked_tickets_for_2week(),count_of_blocked_issues_for_3week,list_of_blocked_tickets_for_3week(),count_of_blocked_issues_for_4weekandmore,list_of_blocked_tickets_for_4weekandmore())

#MIMEMultipart for mail
mail_body = MIMEText(html, 'html')
msg.attach(mail_body)


#Sending Mail
s = smtplib.SMTP('localhost')
s.sendmail(sender, receiver, msg.as_string())
s.quit()
