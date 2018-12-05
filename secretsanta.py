import yaml
import os
import random
import smtplib
import argparse
from email.message import EmailMessage

class SecretSanta(object):
	def __init__(self):
		cwd = os.path.dirname(os.path.abspath(__file__))
		configfile = os.path.join(cwd,'config.yml')
		with open(configfile) as filereader:
			config = yaml.load(filereader)
		self.people = config['people']
		self.pricelimit = config['pricelimit']
		self.template = config['template']
		self.emailconfig = config['emailconfig']
		for person in self.people:
			person['match'] = ''

	def matchpeople(self):
		complete = False
		error = False
		while complete == False or error == True:
			names = [p['name'] for p in self.people]
			for person in self.people:
				match = random.choice(names)
				#this check whether the only option for the last person is themself. 
				#If so, set error = True and break for loop to start again
				if match == person['name'] and len(names) == 1:
					complete = False
					error = True
					break
				while match == person['name']:
					match = random.choice(names)
				person['match'] = match
				names.remove(match)
				error = False
			complete = True
		
	def printmatches(self):
		for person in self.people:
			print('{0}\t-->\t{1}'.format(person['name'],person['match']))

	def rendertemplate(self,persondict):
		emailbody = self.template.format(name=persondict['name'],match=persondict['match'],pricelimit=self.pricelimit)
		return(emailbody)

	def sendemails(self,verbose=False):
		try:
			smtpobj = smtplib.SMTP_SSL(self.emailconfig['smtpserver'],self.emailconfig['smtpport'])
			smtpobj.ehlo()
			smtpobj.login(self.emailconfig['fromemail'],self.emailconfig['smtppwd'])
		except smtplib.SMTPServerDisconnected:
			print('Error, something wrong with configured smtpserver,smtpport')
			raise
		except smtplib.SMTPAuthenticationError:
			print('Error, could not login. Check username/password, check that your account allows insecure apps')
			print('For gmail: Google > my account > Sign-in & security > Connected apps & sites > scroll down and you will find "Allow less secure apps"')
			raise
		for person in self.people:
			msg = EmailMessage()
			msg.set_content(self.rendertemplate(person))
			msg['from'] = self.emailconfig['fromemail']
			msg['to'] = person['email']
			msg['subject'] = self.emailconfig['subject']
			if verbose:
				print('Sending the following email to {0} - {1}: \n\n{2}'.format(person['name'],person['email'],msg.get_content()))
			smtpobj.send_message(msg)
			if verbose:
				print('Email sent')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Secret Santa matching and emailing")
	parser.add_argument('--secret','-s',action='store_true',help='Prevent the displaying of matches')
	args = parser.parse_args()
	ss = SecretSanta()
	acceptable = 'None'
	if args.secret:
		print('People:')
		print(ss.people)
		ss.matchpeople()
	else:
		while acceptable.upper() not in ['Y','']:
			ss.matchpeople()
			print('Current matches:')
			ss.printmatches()
			acceptable = input("Are these ok? ([Y]/N): ")
	send = 'None'
	print('Matching complete')
	while send.upper() not in ['Y','N','']:
		send = input("Would you like to send the emails? ([Y]/N)")
	if send.upper() in ['Y','']:
		if args.secret:
			ss.sendemails(verbose=False)
		else:
			ss.sendemails(verbose=True)
	else:
		print("Exiting without sending")

