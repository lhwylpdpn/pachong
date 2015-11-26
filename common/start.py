import test 
import uuPythonDemo
import configparser
import mail
import time
import winsound
import re
import sys


while(1):
	cf=configparser.ConfigParser()
	cf.read("config.ini")
	opts1=cf.options("config")
	opts2=cf.options("user/pwd")

	network=cf.get("config","network")
	F_frequency=cf.get("config","F_frequency")
	F_province=cf.get("config","F_province")
	F_month=cf.get("config","F_month")
	F_sleep=cf.get("config","sleep")
	#runvoice=0
	pwd=""
	i=0
	for user in opts2:
		
		if len(re.findall("\s_\s\[success\]",cf.get("user/pwd",user)))>0:
			i=i+1
	if len(opts2)==i:
		print("所有学生已经报名成功！程序结束运行")
		sys.exit(0)
	else:

		for user in opts2:
			print(user.split(' _ ')[1],cf.get("user/pwd",user))
			if len(re.findall("\s_\s\[success\]",cf.get("user/pwd",user)))==0:
				process=test.all_start(user.split(' _ ')[1],cf.get("user/pwd",user).split(' _ ')[0],F_province,F_month,F_frequency,network,F_sleep)
			# if process!=1 and runvoice==0:
		# 	# 	runvoice=1
		# 	# 	winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
		mail.run()