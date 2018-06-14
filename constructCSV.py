#!/usr/bin/env python2

# Python Script To Parse Emails and Export Required Key-Value Pairs To a CSV File

from email.parser import Parser
import glob
import csv

dir_path='/home/ubuntu/DATA/enron_mail_20110402/maildir/*/all_documents/*'
messageId = []
date = []
subject = []

def parseEmails():
	with open('/home/ubuntu/DATA/export.csv', 'wb') as csvFile:
		writer = csv.writer(csvFile, delimiter=',')
		for filename in glob.glob(dir_path):
			headers = Parser().parse(open(filename))
		
			messageId.append(headers['message-id'])
			date.append(headers['date'])
			subject.append(headers['subject'])

		Data = zip(messageId, date, subject)

		for lines in Data:
			writer.writerow([lines])

	csvFile.close()

if __name__ == '__main__':
	parseEmails()
