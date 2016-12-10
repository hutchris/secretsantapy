import yaml
import os
import random
import smtplib

class secretsanta(object):
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
			names = []
			for person in self.people:
				names.append(person['name'])
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
		emailsubject = 'Subject: {0}'.format(self.emailconfig['subject'])
		emailbody = self.template.format(name=persondict['name'],match=persondict['match'],pricelimit=self.pricelimit)
		renderedtemplate = '{0}\n{1}'.format(emailsubject,emailbody)
		return(renderedtemplate)

	def sendemails(self,verbose=False):
		try:
			smtpobj = smtplib.SMTP_SSL(self.emailconfig['smtpserver'],self.emailconfig['smtpport'])
			smtpobj.ehlo()
			smtpobj.login(self.emailconfig['fromemail'],self.emailconfig['smtppwd'])
		except smtplib.SMTPServerDisconnected:
			print('Error, something wrong with configured smtpserver,smtpport')
		except smtplib.SMTPAuthenticationError:
			print('Error, could not login. Check username/password, check that your account allows insecure apps')
			print('For gmail: Google > my account > Sign-in & security > Connected apps & sites > scroll down and you will find "Allow less secure apps"')
		except Exception as err:
			print("Unexpected error. Details: {0}".format(repr(err)))
		for person in self.people:
			emailtext = self.rendertemplate(person)
			if verbose:
				print('Sending the following email to {0} - {1}: \n\n{2}'.format(person['name'],person['email'],emailtext))
			smtpobj.sendmail(self.emailconfig['fromemail'],person['email'],emailtext)
			if verbose:
				print('Email sent')

if __name__ == "__main__":
	ss = secretsanta()
	ss.matchpeople()
	acceptable = 'N'
	while acceptable.upper() != 'Y':
		print('Current matches')
		ss.printmatches()
		acceptable = raw_input("Are these ok? (Y/N)")
		if acceptable.upper() != 'Y':
			ss.matchpeople()
	send = raw_input("Would you like to send the emails? (Y/N)")
	if send.upper() == 'Y':
		ss.sendemails(verbose=True)




			

