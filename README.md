# how to use
>>>python Smtp_Mailer.py

## file structure

### config.py
this file has fours variable\n
  >thread_limit = 4  		# the threading limit\n
  >proxy = 0           	# 0: desactivate proxy, 1: activate proxy\n
  >smtpf = "smtp.txt"		# smtp accounts file path\n
  >jobsf = "jobs.txt"		# job file path\n
  >bodyf = "body.txt"		# body file path\n
  
### smtpf
this file hold the credential in the folowing format
[smtp_address]:[user]:[password]:[port]  # port can be 25, 587 or 465

### jobf
this file hold the jobs (the emails to send), in the specific format, "we can change the sender name/email as we want"
[sender_name]:['sender_email']:[receiver_name]:[receiver_email]:[reply_to_email]

### bodyf
this file hold the dynamic message to send, it call dynamic because we have some variabls that change according to each job,
these varibale are:\n
  	'_From'     : it will replaced by the sender name\n
	'_To'       : it will replaced by the receiver name \n
	'_Femail'   : it will replaced by the sender email\n
	'_Temail'   : it will replaced by the receiver email\n
