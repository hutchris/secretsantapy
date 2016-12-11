# secretsantapy
Script to randomly match secret santa participants and send emails

Modify the config.yml file:
Add user/email address combinations, swap out the names and emails with the ones that come in the template. If you need to add more lines, just copy paste a whole line.
people:
  - {name: Chris, email: chrisemail@email.com}
  - {name: Bob, email: bobemail@email.com}
  - {name: Dan, email: danemail@email.com}
  - {name: Jo, email: joemail@email.com}
  
Change the pricelimit to match your secret santa rules.
  
Modify the template if necessary.
 
For the email config, it's easiest to use a gmail account because that has been tested. Just put in your email address and password into the fromemail and smtppwd fields.

run: python secretsanta.py

The script will display an initial secret santa matchup for all users. You can either press Y or N then enter. Pressing N will reshuffle the matches and display the new set. Pressing Y will continue.

It will then ask if you would like to send the emails. Pressing N will cause the script to exit. Pressing Y will send each email and output the body of the email to the screen.
