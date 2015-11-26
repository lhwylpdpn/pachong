# -*- coding: UTF-8 -*-  
from ctypes import *
import sys
import os
import hashlib
import urllib
import string
import zlib
import binascii
import random
import time
import mail
pic_file_path = os.path.join(os.path.dirname(__file__), 'test_pics', 'test.jpg')
s_id  = 106988                 
s_key = "8eae415ec09d447c82d5ef49c7c3caa2"
softVerifyKey="4120110D-C2F8-4FB2-81D1-EBF269B30153"


def getFileMd5(strFile):  
    file = None  
    bRet = False  
    strMd5 = ""  
    try:  
        file = open(strFile, "rb")  
        md5 = hashlib.md5()
        strRead = ""
          
        while True:  
            strRead = file.read(8096)  
            if not strRead:  
                break  
            md5.update(strRead)  
        #read file finish  
        bRet = True  
        strMd5 = md5.hexdigest()  
    except:  
        bRet = False  
    finally:  
        if file:  
            file.close()
  
    return [bRet, strMd5] 

#获取文件CRC32码
def getFileCRC(filename):
    f = None  
    bRet = False
    crc = 0
    blocksize = 1024 * 64
    try:
                f = open(filename, "rb")
                str = f.read(blocksize)
                while len(str) != 0:
                        crc = binascii.crc32(str,crc) & 0xffffffff
                        str = f.read(blocksize)
                f.close()
                bRet = True 
    except:
        print("compute file crc failed!")
        return 0
    return [bRet, '%x' % crc]

#对服务器返回的识别结果进行校验
def checkResult(dllResult, s_id, softVerifyKey, codeid):
    bRet = False
    #服务器返回的是错误代码
    print(dllResult)
    print(len(dllResult))
    if(len(dllResult) < 0):
        return False
    #截取出校验值和识别结果
    items=dllResult.split('_')
    verify=items[0]
    code=items[1]

    localMd5=hashlib.md5(('%d%s%d%s'%(s_id, softVerifyKey, codeid, (code.upper()))).encode("utf8")).hexdigest().upper()
    if(verify == localMd5):
        return code
   
def init():
    
    UUDLL=os.path.join(os.path.dirname(__file__), 'UUWiseHelper.dll')                   #当前目录下的优优API接口文件
    # 加载动态链接库, 需要放在System 的path里，或者当前目录下
    UU = windll.LoadLibrary(UUDLL)
    # 初始化函数调用
    setSoftInfo = UU.uu_setSoftInfoW
    login = UU.uu_loginW
    recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
    getResult = UU.uu_getResultW
    uploadFile = UU.uu_UploadFileW
    getScore = UU.uu_getScoreW
    checkAPi=UU.uu_CheckApiSignW    #api文件校验函数，调用后返回：MD5（软件ID+大写DLL校验KEY+大写随机值参数+优优API文件的MD5值+大写的优优API文件的CRC32值）
    # 初始化函数调用
    
    dllMd5=getFileMd5(UUDLL)   #api文件的MD5值
    dllCRC32=getFileCRC(UUDLL) #API文件的CRC32值
    randChar=hashlib.md5(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()').encode("utf8")).hexdigest()
    checkStatus=hashlib.md5(('%d%s%s%s%s'%(s_id,(softVerifyKey.upper()),(randChar.upper()),(dllMd5[1].upper()),(dllCRC32[1].upper()))).encode("utf8")).hexdigest()     #服务器返回来的值与此值对应一至则表示成功
    serverStatus=c_wchar_p("") #服务器返回来的结果,serverStatus和checkStatus值一样的话，就OK
    #return 3
    #checkAPi(c_int(s_id), c_wchar_p(s_key.upper()),c_wchar_p(randChar.upper()),c_wchar_p(dllMd5[1].upper()),c_wchar_p(dllCRC32[1].upper()),serverStatus)  #调用检查函数,仅需要调用一次即可，不需要每次上传图片都调用一次    pic_file_path = os.path.join(os.path.dirname(__file__), 'test_pics', 'test1.jpg')
    setSoftInfo(s_id,s_key)
    #checkAPi(s_id,s_key,randChar,dllMd5[1],dllCRC32[1],serverStatus)
    #print( "login start "+str(time.strftime("%Y-%m-%d %H:%M:%S")))
    user_i = "ting8882com"
    passwd_i = "tt*963.-+"
    user = c_wchar_p(user_i)  # 授权用户名
    passwd = c_wchar_p(passwd_i)  # 授权密码
    ret = login(user, passwd)
   # print( "login over "+str(time.strftime("%Y-%m-%d %H:%M:%S")))
    if ret < 0:

        print('login error,errorCode:%d' %ret )
    
    result=c_wchar_p("                                              ")  #//分配内存空间，避免内存泄露
    code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(1004),result)
    
    if code_id <= 0:
        save_log("IP被封掉无法访问"+"_"+str(time.strftime("%Y-%m-%d %H:%M:%S")))
        mail.run()
        print('get result error ,ErrorCode: %d' % code_id)
        print('无法获取到验证码图片，请检查是否IP被封掉')
        sys.exit(0)
    else:
        checkedRes=checkResult(result.value, s_id, softVerifyKey, code_id)
    print(str(time.strftime("%Y-%m-%d %H:%M:%S")))
    return checkedRes



def save_log(data):
    file=open("log.ini", "a")
    file.write(data)
    file.close()