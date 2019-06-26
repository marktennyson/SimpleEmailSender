#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  EmailSender.py
#  
#  to use it: save it as `EmailSender.py`. then open terminal and command : `python3 EmailSender.py --start`
#  use linux platform for better result.
#
#
########################################################################
#  Copyright 2019 Mark_Tennyson <mark_baba@rediffmail.com>             #
#  								                                       #
#  EmailSender is a free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License as      #
#  published by the Free Software Foundation; either version 2 of      #
#  the License, or (at your option) any later version.		           #
#                                                                      #
#  This program is distributed in the hope that it will be useful,     #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of      #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       #
#  GNU General Public License for more details.                        #
#                                                                      #  
#  You should have received a copy of the GNU General Public License   #
#  along with this program; if not, write to the Free Software         #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,          #
#  MA 02110-1301, USA.                                                 #
########################################################################

import os
import sys
import base64
import smtplib 
from colorama import *
from getpass import getpass
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders as _ENCODERS
from time import sleep as slp
try:
	from pyfiglet import figlet_format as _FIGLET
except:
	os.system("pip install pyfiglet")
	from pyfiglet import figlet_format as _FIGLET

red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
magenta = Fore.MAGENTA
blue = Fore.BLUE
yellow = Fore.YELLOW
reset = Style.RESET_ALL
_LOGO = _FIGLET("    Email Sender", font = "bulbhead")
_LOGO = green+_LOGO

Our_SMTP_Service_Server_Name = ["smtp.gmail.com", "smtp.mail.yahoo.com", "smtp-mail.outlook.com."]

_SMTP_PORT = 587

def help_HELP():
	print (yellow+"""
	1. start  ========  to send a email
	2. help   ========  to know the command
	3. logout ========  to logging out
		"""+reset)

def error_Printing(_ERROR):
	print ("\n"+red+"[ERROR]" +reset+" SORRY ! We Are Unable To Login With Your Credentials\n")
	if "535" in _ERROR:
		print ("\n"+red+"[ERROR]" +reset+" Invalid User_ID or Password\n")
	elif "Connection unexpectedly closed" in _ERROR:
		print ("\n"+red+"[ERROR]" +reset+" Your Server Is Not Receiving Connection\n")
	else: print ("\n"+red+"[ERROR]" +reset+" SomeThing Went Wrong\n")
	print ("\n"+blue+"[INFO]"+reset+" You Should Turn Off Your '2 step authentication' \n")
	print ("\n"+blue+"[INFO]"+reset+" For Gmail Visit => 'https://myaccount.google.com/lesssecureapps'\n       And Turn It On.\n")
	os._exit(0)

def receipient_Interact_and_Send_MAIL(_SMTP_CONNECTION, _USER_ID):
	_RECIPIENT_ID,_BCC_RECIPIENT_ID = receiver_Details()
	_FINAL_TEXT = creating_Message_Contents(_USER_ID,_RECIPIENT_ID)
	_SMTP_CONNECTION.sendmail(_USER_ID, _BCC_RECIPIENT_ID, _FINAL_TEXT)
	print ("\n"+green+"[SUCCESS]"+reset+" Successfully Send Your Mail To => {}".format(_RECIPIENT_ID))

def receiver_Details():
	_BCC_ID_LIST = []
	while True:
		try:
			_RECEIVER_ID = raw_input(cyan+"\nEnter Receiver's Email ID: "+reset)
		except:
			_RECEIVER_ID = input(cyan+"\nEnter Receiver's Email ID: "+reset)
		if _RECEIVER_ID =="" or "@" not in _RECEIVER_ID:
			print ("\n"+blue+"[INFO]"+reset+" Email Address Must Have => '@'\n")
			continue
		else: break
	while True:
		try:
			_BCC_ID_PATH = raw_input(cyan+"\nBCC: "+yellow+"(`Enter` To Avoid/Insert path): "+reset)
		except:
			_BCC_ID_PATH = input(cyan+"\nBCC: "+yellow+"(`Enter` To Avoid/Insert path): "+reset)
		if not _BCC_ID_PATH:
			_BCC_ID_LIST.append(_RECEIVER_ID)
			return (_RECEIVER_ID,_BCC_ID_LIST)
			break
		if os.path.exists(_BCC_ID_PATH):
			with open(_BCC_ID_PATH) as _BCC:
				_BCC_DATA = _BCC.readlines()
			for _BCC_ID_FOR_CHECKING in _BCC_DATA:
				if "@" not in _BCC_ID_FOR_CHECKING:
					print ("\n"+red+"[ERROR]" +reset+"Unable To Send Mail To => {}".format(_BCC_ID_FOR_CHECKING))
					_BCC_ID_FOR_CHECKING = ""
				_DATA = _BCC_ID_FOR_CHECKING.rstrip()
				_BCC_ID_LIST.append(_DATA)
				_BCC_ID_LIST.append(_RECEIVER_ID)
				try: 
					_BCC_ID_LIST.remove("")
				except:
					pass
				return (_RECEIVER_ID,_BCC_ID_LIST)
		else:
			print ("\n"+red+"[ERROR]" +reset+"Invalid Path. Check And ReEnter\n")
			continue

def other_Server_Name_Adder():
	print ("\n"+blue+"[INFO]"+reset+" By Default We Only Providing Service For Gmail, Yahoo and Outlook\n")
	slp(0.68)
	print ("\n"+blue+"[INFO]"+reset+" If You Want To Using Another Service Please Enter Your SMTP SERVER Name\n")
	slp(0.68)
	while True:
		try:
			OTHER_SERVER = raw_input(cyan+"\nEnter Your Own Server Name: "+reset)
		except:
			OTHER_SERVER = input(cyan+"\nEnter Your Own Server Name: "+reset)
		if not OTHER_SERVER:
			print ("\n"+blue+"[INFO]"+reset+" Enter A Valid Server Name\n")
			continue
		else:
			print ("\n"+blue+"[INFO]"+reset+" You Entered Yor Server name =>"+green+ " {}\n".format(OTHER_SERVER))
			print (reset)
			slp(.5)
		try:
			_ANSWER = raw_input(cyan+"\nAre You Want To Continue"+yellow+" (yes/no)=> "+reset)
			_ANSWER = _ANSWER.lower()
		except:
			_ANSWER = input(cyan+"\nAre You Want To Continue"+yellow+" (yes/no)=> "+reset)
			_ANSWER = _ANSWER.lower()
		if _ANSWER =="" or _ANSWER == "yes" or _ANSWER == "y":
			print ("\n"+green+"[SUCCESS]"+reset+" SERVER Name Set To {}\n".format(OTHER_SERVER))
			Our_SMTP_Service_Server_Name.append(OTHER_SERVER)
			break
		elif _ANSWER == "no" or _ANSWER == "n":
			continue
		else :
			print ("\n"+red+"[ERROR]" +reset+" Invalid Input")
			continue

def check_SMTP_Server_Name(USER_ID):
	if "gmail" in USER_ID:
		_SERVER = Our_SMTP_Service_Server_Name[0]
	elif "yahoo" in USER_ID:
		_SERVER = Our_SMTP_Service_Server_Name[1]
	elif "outlook" in USER_ID:
		_SERVER = Our_SMTP_Service_Server_Name[2]
	else:
		_SERVER = Our_SMTP_Service_Server_Name[3]
	return _SERVER

def creating_Message_Contents(_USER_ID, _RECEIVER_ID):
	_MESSAGE = MIMEMultipart()
	try:  #for python2
		_SUBJECT = raw_input(cyan+"\nEnter The Subject"+yellow+"(Press Enter To Avoid): "+reset)
		if _SUBJECT == "":
			_SUBJECT = "(no_subject)"
			print ("\n"+blue+"[INFO]" +reset+" Sending Without Subject")
		_BODY = raw_input(cyan+"\nMessage"+yellow+"(Press `Enter` To Avoid/Add Plain Text/Insert Path To Read): "+reset)
		if _BODY == "":
			_BODY = " "
			print ("\n"+blue+"[INFO]" +reset+" Sending Without Body")
			_MESSAGE.attach(MIMEText(_BODY, 'plain'))
		elif os.path.exists(_BODY):
			print ("\n"+blue+"[INFO]" +reset+" Added The File Data")
			with open(_BODY) as _FILE:
				_DATA = _FILE.read()
				#_BODY_TEXT_ = _DATA
			if _BODY.endswith(".html") or _BODY.endswith(".htm"):
				_MESSAGE.attach(MIMEText(_DATA, 'html'))
			else:
				_MESSAGE.attach(MIMEText(_DATA, 'plain'))
		else:
			_MESSAGE.attach(MIMEText(_BODY, 'plain'))
		while True:
			_ATTACHMENT_PATH = raw_input(cyan+"\nEnter Your Attachment's path"+yellow+"(Press Enter To Avoid): "+reset)
			if _ATTACHMENT_PATH != "":
				if os.path.exists(_ATTACHMENT_PATH):
					#print ("path exists")
					break
				else:
					print ("\n"+red+"[ERROR]" +reset+" Invalid Path! Check AND ReEnter")
					continue
			else : break
		if _ATTACHMENT_PATH != "":
			while True:
				try:
					_FILENAME = raw_input(cyan+"\nEnter A File Name With Proper Extension: "+reset)
				except:
					_FILENAME = input(cyan+"\nEnter A File Name With Proper Extension: "+reset)
				if _FILENAME == "" or "." not in _FILENAME:
					print ("\n"+red+"[ERROR]" +reset+" Enter A Valid File Name")
					continue
				else: break
		
	except: #for python3
		_SUBJECT = input(cyan+"\nEnter The Subject"+yellow+"(Press Enter To Avoid): "+reset)
		if _SUBJECT == "":
			_SUBJECT = "(no_subject)"
			print ("\n"+blue+"[INFO]" +reset+" Sending Without Subject")
		_BODY = input(cyan+"\nMessage"+yellow+"(Press `Enter` To Avoid/Add Plain Text/Insert Path To Read): "+reset)
		if _BODY == "":
			_BODY = " "
			print ("\n"+blue+"[INFO]" +reset+" Sending Without Body")
			_MESSAGE.attach(MIMEText(_BODY, 'plain'))
		elif os.path.exists(_BODY):
			print ("\n"+blue+"[INFO]" +reset+" Added The File Data")
			with open(_BODY) as _FILE:
				_DATA = _FILE.read()
				#_BODY_TEXT_ = _DATA
			if _BODY.endswith(".html") or _BODY.endswith(".htm"):
				_MESSAGE.attach(MIMEText(_DATA, 'html'))
			else:
				_MESSAGE.attach(MIMEText(_DATA, 'plain'))
		else:
			_MESSAGE.attach(MIMEText(_BODY, 'plain'))
		while True:
			_ATTACHMENT_PATH = input(cyan+"\nEnter Your Attachment's path"+yellow+"(Press Enter To Avoid): "+reset)
			if _ATTACHMENT_PATH != "":
				if os.path.exists(_ATTACHMENT_PATH):
					#print ("path exists")
					break
				else:
					print ("\n"+red+"[ERROR]" +reset+" Invalid Path! Check AND ReEnter")
					continue
			else : break
		if _ATTACHMENT_PATH != "":
			while True:
				try:
					_FILENAME = raw_input(cyan+"\nEnter A File Name With Proper Extension: "+reset)
				except:
					_FILENAME = input(cyan+"\nEnter A File Name With Proper Extension: "+reset)
				if _FILENAME == "" or "." not in _FILENAME:
					print ("\n"+red+"[ERROR]" +reset+" Enter A Valid File Name")
					continue
				else: break
	
	_MESSAGE ['From'] = _USER_ID
	_MESSAGE['To'] = _RECEIVER_ID
	_MESSAGE['Subject'] = _SUBJECT 
	_MESSAGE['Bcc'] = _RECEIVER_ID
	try:
		_ATTACHMENT = open(_ATTACHMENT_PATH, "rb")
		_PAYLOAD = MIMEBase('application', 'octet-stream')
		_PAYLOAD.set_payload((_ATTACHMENT).read())
		_ENCODERS.encode_base64(_PAYLOAD)
		_PAYLOAD.add_header('Content-Disposition', 'attachment', filename= "{}".format(_FILENAME))
		_MESSAGE.attach(_PAYLOAD)
	except:
		print ("\n"+blue+"[INFO]"+reset+" No Attachment\n")
		pass
	_TEXT = _MESSAGE.as_string()
	return _TEXT

def users_Details():
	while True:
		try :
			USER_ID = raw_input(cyan+"\nEnter Your Email ID: "+reset)
		except:
			USER_ID = input(cyan+"\nEnter Your Email ID: "+reset)
		if not USER_ID or "@" not in USER_ID:
			print ("\n"+blue+"[INFO]"+reset+" Enter A Valid USER_ID\n")
			continue
		else:
			break
	SPLIT_LIST = USER_ID.split("@")
	if SPLIT_LIST[1] != "gmail.com" and SPLIT_LIST[1] != "yahoo.com" and SPLIT_LIST[1] != "outlook.com":
		other_Server_Name_Adder()
	while True:
		USER_PASSWD = getpass(cyan+"\nEnter Your Password: "+reset)
		if not USER_PASSWD: continue
		else: break
	return (USER_ID,USER_PASSWD)

def main():
	os.system("clear")
	
	try:
		_INPUT = sys.argv[1]
		_INPUT = _INPUT.lower()
	except:
		print (green+"try : '--start  ===  to START it'\n"+reset)
		os._exit(0)
	if  "-start" in _INPUT:
		print (_LOGO)
		print (green+"		Author:"+blue+" {"+yellow+" Mark_Tennyson"+cyan+" <=>"+magenta+" mark_baba@rediffmail.com"+blue+" }"+reset)
		print (red+"      	  	version : 1.0.2"+reset)
		_USER_ID, _USER_PASSWD = users_Details()
		_SERVER_NAME = check_SMTP_Server_Name(_USER_ID)
		_SMTP_CONNECTION = smtplib.SMTP(_SERVER_NAME,_SMTP_PORT)
		_SMTP_CONNECTION.ehlo()
		_SMTP_CONNECTION.starttls()
		try:
			_SMTP_CONNECTION.login(_USER_ID,_USER_PASSWD)
			print ("\n"+green+"[SUCCESS]"+reset+" You Are Successfully Logged In\n")
		except Exception as e:
			e=str(e)
			error_Printing(e)
		while True:
			print ("\n"+blue+"[INFO]"+reset+" Type `help` To Know More\n")
			try:
				_CMD = raw_input(cyan+"\nEnter What You Want: "+reset)
			except:
				_CMD = input(cyan+"\nEnter What You Want: "+reset)
			_CMD == _CMD.lower()
			
			if "logout" in _CMD or "3" in _CMD:
				print ("\n"+blue+"[INFO]"+reset+"Logging Out\n")
				slp(1)
				_SMTP_CONNECTION.quit()
				os._exit(0)
			elif "help" in _CMD or "2" in _CMD:
				help_HELP()
			elif "start" in _CMD or "1" in _CMD:
				receipient_Interact_and_Send_MAIL(_SMTP_CONNECTION,_USER_ID)
			else:
				print ("\n"+red+"[ERROR]" +reset+" Invalid Input")
	else:
		print (green+"try : '--start  ===  to START it'\n"+reset)
		os._exit(0)

if __name__ == '__main__':
	main()