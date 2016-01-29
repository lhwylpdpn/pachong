import urllib.parse
import urllib.request
import sys
import uuPythonDemo
import time
import datetime
import http.cookiejar
import random
import re
import os
import mail
import configparser
import voice
# coding=gbk
# url = 'http://toefl.etest.net.cn/cn/TOEFLAPP'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# values = {'username':'4018060','password':'Zing@821004'}
# headers = { 'Cookie' : 'Cookie:BIGipServertoefl_internal_pub=2684397760.20480.0000; WebBrokerSessionID=ketMSePUSTC5r8Ot' }
# data = urllib.parse.urlencode(values).encode(encoding='UTF8')
# req = urllib.request.Request(url, data, headers)
# response = urllib.request.urlopen(req)
# the_page=response.read()
# print(the_page.decode("GBK"))
global log_txt
log_txt=""
global log_new
log_new=""
#####################################################
#第一次获取验证码失败记录1
#首页登录失败记录2
#请求省份列表失败记录3
#第二次获取验证码失败记录4
#查询考场请求失败记录5
#占座失败记录6
#发送占座成功，但是系统返回失败8
#####################################################
def ChinaBiddingLogin(usename,pwd,province,month,network,count,sleep,day):
	global log_txt
	global log_new
	url_choose="toefl.etest."+network+".cn"
	webCookie = http.cookiejar.LWPCookieJar()  
	openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(webCookie),urllib.request.HTTPHandler)
	user_agent=[]
	user_agent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50")
	user_agent.append("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50")
	user_agent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0")
	user_agent.append("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)")
	user_agent.append("Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0")
	user_agent.append("Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")
	user_agent.append("Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11")
	user_agent.append("Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)")
	user_agent.append("Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
	user_agent.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
	random.shuffle(user_agent)
	send_header = {'Host':url_choose,'User-Agent':user_agent[1],'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive'}
	#urlopener.addheaders.append(('Referer', 'http://www.chinabidding.com.cn/zbw/login/login.jsp'))
	#urlopener.addheaders.append(('Accept', 'text/html, application/xhtml+xml, */*'))
	#urlopener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
	#urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
	#urlopener.addheaders.append(('Host', 'www.chinabidding.com.cn'))i
	#urlopener.addheaders.append(('Connection', 'Keep-Alive'))
	urllib.request.install_opener(openner)
	imgurl="http://"+url_choose+"/cn/"+str(time.time()*1000)[0:13]+str(random.random())+"VerifyCode3.jpg"
#获取登录验证码的请求
	#print(imgurl)
	req1 = urllib.request.Request(imgurl,headers=send_header)
	i=0
	while i<int(count):
		try:
			response1=urllib.request.urlopen(req1)
			
		except Exception as e:
			log_txt=log_txt+"1"
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤一：第一次获取登录验证码失败"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤一：第一次获取登录验证码失败")
			i=i+1;time.sleep(int(sleep))
		else:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤一：第一次获取登录验证码成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤一：第一次获取登录验证码成功")
			break
	else:
		return 0
	save_file(response1.read())
	verifycode=uuPythonDemo.init()
	url = 'http://'+url_choose+'/cn/TOEFLAPP'
	values = {'username':usename,'__act':'__id.24.TOEFLAPP.appadp.actLogin','password':pwd,'LoginCode':verifycode,'submit.x':'14','submit.y':'8'}
	data = urllib.parse.urlencode(values).encode(encoding='UTF8')
#第一次登录的请求
	req = urllib.request.Request(url, data,send_header)
	i=0
	while i<int(count):
		try:
			response = urllib.request.urlopen(req)
			
		except Exception as e:
			log_txt=log_txt+"2"
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤二：登录失败"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤二：登录失败")
			i=i+1;time.sleep(int(sleep))
		else:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤二：登录成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤二：登录成功")
			break
	else:
		return 0
#跳转到选择考场的请求	
	url = 'http://'+url_choose+'/cn/Information?page=SeatsQuery'
	req = urllib.request.Request(url,headers=send_header)
	
	i=0
	while i<int(count):
		try:
			response = urllib.request.urlopen(req)
			the_page=response.read()
			save_html(the_page,33)
			p=re.findall("\d{5}.\d{10}.VerifyCode2.jpg",the_page.decode("GBK"))
			sb=str(p[0])
		except Exception as e:
			log_txt=log_txt+"3"
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤三：查看省份页面显示失败"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤三：查看省份页面显示失败")
			i=i+1;time.sleep(int(sleep))
		else:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤三：查看省份页面显示成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤三：查看省份页面显示成功")
			break
	else:
		return 0

#第二次获取验证码的请求
	i=0
	while i<int(count):
		try:
			
			req1 = urllib.request.Request("http://"+url_choose+"/cn/"+p[0],headers=send_header)
			response1=urllib.request.urlopen(req1)
			
		except Exception as e:
			log_txt=log_txt+"4"
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤四：第二次获取验证码失败"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤四：第二次获取验证码失败")
			i=i+1;time.sleep(int(sleep))
		else:
			
			print(time.strftime("%Y-%m-%d %H:%M:%S"))
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤四：第二次获取验证码成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤四：第二次获取验证码成功")
			break
	else:
		return 0
	save_file(response1.read())
	verifycode=uuPythonDemo.init()
#配置参数、省份、时间
	url= 'http://'+url_choose+'/cn/SeatsQuery?mvfAdminMonths='+month+'&mvfSiteProvinces='+province+'&whichFirst=AS&afCalcResult='+verifycode+'&__act=__id.34.AdminsSelected.adp.actListSelected&submit.x=21&submit.y=9'
	#print(url)
	req = urllib.request.Request(url,headers=send_header)
	i=0
	while i<int(count):

		try:
			response = urllib.request.urlopen(req)
		except Exception as e:
			log_txt=log_txt+"5"
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤五：查询考位失败"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤五：查询考位失败")
			i=i+1;time.sleep(int(sleep))
		else:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤五：查询考位成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤五：查询考位成功")
			the_page=response.read()
			save_html(the_page,"buzhou5"+str(random.random()))
			#print(the_page)
			time.sleep(int(sleep))
			p=re.findall("\w+\=\""+day+"\w+\=\w+\"\>\s+\<\w+\s\w+\=\"\w+\"\s\w+\=\"\w+\"\s\w+\=\"[\u4e00-\u9fa5]+\"\s\w+\=\"\w+.__act.value=\'\w+.\w+.\w+.\w+.\w+.\w+.\w+.\w+.\w+\';\w+\s\w+\(\);\"\>",the_page.decode("GBK"))
			q=re.findall("lick\=[\u4e00-\u9fa5_a-zA-Z0-9()\.\;\"\s\=\']+disabled",the_page.decode("GBK"))
			print(len(q),len(p))
			if len(p)>0:
				form_name=str(p[0])
				voice.init()
				break
			elif len(p)<=0 and len(q)>0:
				print("步骤五：查询考位成功，但是已经没有位置了")
				return 0
			else:
				form_name=""
				time.sleep(6)
				print("步骤五:查询等待图片时间超时,需要重新登录")
				return 0
	else:
		return 0
	#print( time.strftime("%Y-%m-%d %H:%M:%S"))
	
	while i<int(count):	
		try:

			#form_name=register_all(the_page.decode("GBK"))
			#print(form_name[7:26])
			#print(form_name[122:193])
			print(form_name[7:26],re.findall("SITE.[\u4e00-\u9fa5_a-zA-Z0-9（）()\s\.]+actRegister",form_name)[0])
			values = {'siteadmin':str(form_name[7:26]),'__act':re.findall("SITE.[\u4e00-\u9fa5_a-zA-Z0-9（）()\s\.]+actRegister",form_name)[0]}
			data = urllib.parse.urlencode(values).encode(encoding='UTF8')
			req = urllib.request.Request(url,data,send_header)
			response=urllib.request.urlopen(req)
		except Exception as e:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤六：提交占考位请求失败"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤六：提交占考位请求失败")
			i=i+1;time.sleep(int(sleep))
		else:
			log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤六：提交占考位请求成功"+"\n"
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤六：提交站考位请求成功")
			the_page=response.read()
			save_html(the_page,"buzhou6"+str(random.random()))
			if len(re.findall("请继续操作，直至完成付款确认。",the_page.decode("GBK")))>0 and len(re.findall(form_name[17:26],the_page.decode("GBK")))>0:
				log_txt=log_txt+"T"
				p=re.findall("\<\w+\s\w+\=\"3\"\s\w+\=\"#EEEEEE\"\>[\u4e00-\u9fa5_a-zA-Z0-9（）()\s]+",the_page.decode("GBK"))
				try:
					print(p[3].split('>')[1])
					print(p[4].split('>')[1])
					log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤七：经过再次验证占考位已成功！"+"\n"
					print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤七：经过再次验证占考位已成功！")
					save_mail("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]  [账号:"+str(usename)+"]  [密码:"+str(pwd)+"] [考试时间："+p[0].split('>')[1]+p[1].split('>')[1]+"] [考试地点："+p[3].split('>')[1]+"_"+p[4].split('>')[1]+"]\n")
					save_successlog("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]  [账号:"+str(usename)+"]  [密码:"+str(pwd)+"] [考试时间："+p[0].split('>')[1]+p[1].split('>')[1]+"] [考试地点："+p[3].split('>')[1]+"_"+p[4].split('>')[1]+"]\n")
					update_config(usename)
					break
					return form_name[17:26]
				except Exception as e:
					print(e)
					#print("注意，程序错误，有可能已经占上考位，但是考点信息获取出错",usename,pwd)
			else:
				log_new=log_new+"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤七：经验证,占考位失败,服务器忙"+"\n"
				print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]"+"步骤七：经验证,占考位失败,服务器忙")
				log_txt=log_txt+"8"
				i=i+1;time.sleep(2)
	else:
		return 0	


def update_config(name):
	cf=configparser.ConfigParser()
	cf.read("config.ini")
	opts2=cf.options("user/pwd")
	user=re.findall("\w+\s\_\s"+str(name),";".join(opts2))
	print(user[0])
	cf.set("user/pwd",user[0],str(cf.get("user/pwd",user[0]))+" _ [success]")
	cf.write(open("config.ini","w"))


def save_file(data):
    file=open("test_pics/test.jpg", "wb")
    file.write(data)
    file.flush()
    file.close()
def save_html(data,name):
    file=open("htmllog/"+str(name)+"s.html", "wb")
    file.write(data)
    file.flush()
    file.close()

def save_log(data):
    file=open("log.ini", "a")
    file.write(data)
    file.close()
def save_mail(data):
    file=open("mail.ini", "a")
    file.write(data)
    file.close()
def save_successlog(data):
    file=open("successlog.ini", "a")
    file.write(data)
    file.close()
def register_all(page):
	global log_txt
	global log_new
	p=re.findall("\w+\=\"\w+\=\w+\"\>\s+\<\w+\s\w+\=\"\w+\"\s\w+\=\"\w+\"\s\w+\=\"[\u4e00-\u9fa5]+\"\s\w+\=\"\w+.__act.value=\'\w+.\w+.\w+.\w+.\w+.\w+.\w+.\w+.\w+\';\w+\s\w+\(\);\"\>",page)
	q=re.findall("onclick\=[\u4e00-\u9fa5_a-zA-Z0-9()\.\;\"\s\=\']+disabled\=\"\"\>",page)
	if len(q)>0:
		try:
			#print(p[0])
			#print(p[1])
			return str(p[0])
		except Exception as e:
			log_txt=log_txt+"6"
			print(e,"查询位置页面的时候出错了")
		







def all_start(usename,pwd,province,month,count,network,sleep,day):
	global log_txt
	global log_new
	i=1
	process_all=ChinaBiddingLogin(usename,pwd,province,month,network,count,sleep,day)
	#while process_all==1 and i<=int(count):
	#	process_all=ChinaBiddingLogin(usename,pwd,province,month,network,count)
	#	i=i+1;time.sleep(int(sleep))
	print(log_txt)
	#save_log(usename+"_"+log_txt+"_"+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"_"+str(process_all)+"\n")
	save_log(usename+"_"+log_new)
	#if process_all!=1:
		#save_mail("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]  [账号:"+str(usename)+"]  [密码:"+str(pwd)+"]  [省份:"+str(province)+"]  [月份:"+str(month)+"] [时间与编号:"+str(process_all)+"]"+"\n")
	log_new=""
	log_txt=""
	return process_all

# if __name__ == '__main__':
	
# 	file=open("test.html", "r")
# 	tt=file.read()

# 	p=re.findall("请继续操作，直至完成付款确认。",tt)
# 	p2=re.findall("STN80055E",tt)
# 	file.close()
