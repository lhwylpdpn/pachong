import urllib.parse
import urllib.request
import ssl
import time
import hmac
import hashlib
import base64
import http.cookiejar
import random
import sys
print("config_"+sys.argv[1]+".ini")
#from urllib import urlencode
ssl._create_default_https_context = ssl._create_unverified_context
def test(url):
	uu=url
	req=urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	print(response.read())
def hmacsha1():
	url="http://api-content.dfs.kuaipan.cn/1/fileops/download_file"
	d={"name":url}
	url2=urllib.parse.urlencode(d)
#str(time.time())[0:10]
	nonce="".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 8)).replace(' ','')
	data={"oauth_nonce":nonce,"oauth_timestamp":str(time.time())[0:10],"oauth_consumer_key":"xcGxCMkJ9h7JrMTi","oauth_signature_method":"HMAC-SHA1","oauth_version":"1.0","oauth_token":"033b9f1c6a41084a515f812e","root":"app_folder","path":"config_"+sys.argv[1]+".ini"}
	d2={"name":"&".join(k+"="+data[k] for k in sorted(data.keys()))}
	url3=urllib.parse.urlencode(d2)
	w_data="GET&"+url2[5:]+"&"+url3[5:]
	#print(w_data)
	B_base=hmac.new(bytes("qia7IEHyN5cJBzPa&2382add7a9e848b3aa87ce95050a1fb5","utf-8"),w_data.encode("utf-8"),hashlib.sha1).digest()
	B_base=base64.b64encode(B_base)
	d4={"name":B_base}
	url4=urllib.parse.urlencode(d4)
	#print(url4[5:])
	w_data=url+"?"+"oauth_signature="+url4[5:]+"&"+"&".join(k+"="+data[k] for k in sorted(data.keys()))
	save_file2(w_data)

	webCookie = http.cookiejar.LWPCookieJar()  
	openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(webCookie),urllib.request.HTTPHandler)
	send_header = {'Host':"http://api-content.dfs.kuaipan.cn",'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive'}
	urllib.request.install_opener(openner)
	response=urllib.request.urlopen(w_data)
	save_file(response.read())
def save_file(data):
    file=open("config.ini", "wb")
    file.write(data)
    file.flush()
    file.close()
def save_file2(data):
    file=open("w_data.ini", "w")
    file.write(data)
    file.flush()
    file.close()
if __name__ == '__main__':
	#test("https://openapi.kuaipan.cn/open/requestToken?oauth_signature=FmKpASqG6revPOWA9hhn9E%2BPqx0%3D&oauth_consumer_key=xcGxCMkJ9h7JrMTi&oauth_nonce=F8J8eHpf&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1444291739&oauth_version=1.0")
	hmacsha1()
