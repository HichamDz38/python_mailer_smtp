#!usr/bin/python 
# -*- coding: utf-8 -*-
import threading,sys, smtplib, socket, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from threading import Thread
socket.setdefaulttimeout(15)    # smtp default timeout, change number to speed up large lists
from config import*
import random
import re


# load accounts credential from smtpf file
accounts=[]
try: 
	L=open(smtpf)
	l=L.readline()
	while l!='':
		accounts.append(l.replace("\n",""))
		l=L.readline()
	L.close()
except: 
	print("\n[+] We were unable to open the smtp file. Check again your path and try again.")

# load jobs from jobsf file
try: 
	L=open(jobsf)
	jobs = L.read().split('\n')
	L.close()
except: 
	print("\n[+] We were unable to open the jobs file. Check again your path and try again.")

# load body from bodyf file
try: 
	L=open(bodyf, encoding="utf8")  # unicode support
	subject1, body1 = L.read().split("\n#\n")
	subject1 = subject1
	body1 = body1
	L.close()
except Exception as e: 
	print("\n[+] We were unable to open the file. Check again your path and try again.",bodyf,e)

print("limit number of thread is : ",thread_limit)


def timer():
	""" get the actual time"""
    now = time.localtime(time.time())
    return time.asctime(now)

def get_smtp(index=random.randint(0,len(accounts)-1)):
	"""return a random account from the accounts list"""
	return accounts[index]


def get_proxy(index):
	""" return a random proxy from the proxies list"""
	return proxies[index%len(proxies)]


def sendchk(body, subject, job):   # seperated function for checking
	""" this is the main function that send email
	it's need three arguments:
	body, subject, job"""
	global N,jobs
	Err_N=0
	while True:
		try:
			# get credential from file
			host,user,password,prt = get_smtp(N).split(':')
			if prt == "465":
	                    smtp = smtplib.SMTP_SSL(host,int(prt))
			else:
	                    smtp = smtplib.SMTP(host,int(prt))
			smtp.login(user, password)
			code = smtp.ehlo()[0]
			if not (200 <= code <= 299):
				code = smtp.helo()[0]
				if not (200 <= code <= 299):
					raise SMTPHeloError(code, resp)
			fromaddr = job[1]  # sender
			toaddr = job[3]  # receiver
			reply = job[4]  # repley to
			msg= MIMEText(body, 'plain', 'utf-8')
			msg['Subject'] = subject  # the email's subject
			msg['To'] = formataddr([job[2], job[3]])  # receiver name, receiver email 
			msg['From'] = formataddr([job[0], job[1]])  # sender name, sender email
			msg['Reply-to'] = formataddr([job[0], job[4]])  # reply to name, reply to email
			smtp.sendmail(fromaddr, toaddr, msg.as_string())  # send the email
			print("\n\t\t[!] Email Sent Successfully:",host, user, password)
			smtp.quit()
			Err_N=0
			return
		except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as msg:
			print(msg)
			print("[-]\t\tLogin Failed:",host, user, password)
			N=(N+1)%len(accounts)
			Err_N+=1
			if Err_N>len(accounts):
				print("all your smtp not working , or there is a problem with connection")
				return
			print("Try with other smtp")


N = 0  # hold the account index
L_th = []  # hold the active threads
print("[!] Start at: " + timer() + "")
for j in jobs:
	if j!="":
		job=j.split(":")
		try:
			body = re.sub('_From', job[0], body1)
			body = re.sub('_To', job[2], body)
			body = re.sub('_Femail', job[1], body)
			body = re.sub('_Temail', job[3], body)
			subject = re.sub('_From', job[0], subject1)
			subject = re.sub('_To', job[2], subject)
			subject = re.sub('_Femail', job[1], subject)
			subject = re.sub('_Temail', job[3], subject)
			print(get_smtp(N).split(":"))
			print("\n\t[+] start thread",":".join(job))
			th=Thread(target=sendchk,args=(body,subject,job,))
			L_th.append(th)
			th.start()
			while threading.active_count() >=thread_limit:
				pass
		except Exception as e:
			print('\n[+] We have found a error in your accounts list')
			print('\n[!] IMPORTANT: THE SMTP ACCOUNTS MUST BE IN THE FOLLOWING FORMAT : IP:USER:PASS:PORT')
			print(e)
		N=(N+1)%len(accounts)


# wait for all threads to done
for i in L_th:
	i.join()
print("[!] Ended at: " + timer() + "")
print("reformat the smtp file")

N = (N-1)%len(accounts)
accounts=accounts[N+1:]+accounts[:N+1]
L=open(smtpf,"w")
for i in accounts:
	L.write(i+"\n")
L.close()
