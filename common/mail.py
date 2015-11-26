
import smtplib
import time
import configparser
from email.mime.text import MIMEText  

cf=configparser.ConfigParser()
cf.read("config.ini")
opts1=cf.options("config")
opts2=cf.options("user/pwd")

network=cf.get("config","network")
F_frequency=cf.get("config","F_frequency")
F_province=cf.get("config","F_province")
F_month=cf.get("config","F_month")

mail_host="smtp.126.com"  #设置服务器
mail_user="manyadaibao"    #用户名
mail_pass="59421ting"   #口令 
mail_postfix="126.com"  #发件箱的后缀
  
def send_mail(sub,content):  
    to_list=["manyadaibao@126.com"]
    me="自动化占位程序"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    print(msg.as_string())
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print (str(e))  
        return False  

def run():
    file=open("mail.ini")
    t=file.readlines()
    if len(t)>0:
        send_mail("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"][省份："+F_province+"][占位情况]","".join(t))

    file.close()
    file=open("mail.ini","w")
    file.write('')
    file.close()