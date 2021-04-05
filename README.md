# how to use
>python Smtp_Mailer.py

## file structure

- ### config.py
this file has fours variable  
  >**thread_limit = 4  		# the threading limit  
  >**proxy** = 0           	# 0: desactivate proxy, 1: activate proxy  
  >**smtpf** = "smtp.txt"		# smtp accounts file path  
  >**jobsf** = "jobs.txt"		# job file path  
  >**bodyf** = "body.txt"		# body file path  
  
- ### smtpf
this file hold the credential in the folowing format
[smtp_address]:[user]:[password]:[port]  # port can be 25, 587 or 465

- ### jobf
this file hold the jobs (the emails to send), in the specific format, "we can change the sender name/email as we want"
[sender_name]:[sender_email]:[receiver_name]:[receiver_email]:[reply_to_email]

- ### bodyf
this file hold the dynamic message to send, it call dynamic because we have some variabls that change according to each job,
these varibale are:  
  	> **_From**      : it will replaced by the sender name   
	> **_To**        : it will replaced by the receiver name  
	> **_Femail**    : it will replaced by the sender email  
	> **_Temail**    : it will replaced by the receiver email  
