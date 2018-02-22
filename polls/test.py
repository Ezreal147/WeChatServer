import execjs
import requests
import time
import random
import json
import rsa
import binascii
from bs4 import BeautifulSoup
import pickle
import os

session = requests.session()
username = '20160421543'
pwd = '12345yy'


def saveCookies(cookies):
	f = open('/home/testproject/polls/cookies.txt', 'wb+')
	pickle.dump(cookies, f)
	f.close()
def getCookies():
	f = open('/home/testproject/polls/cookies.txt', 'rb+')
	cookies = pickle.load(f)
	f.close()
	return cookies


def getcsrftoken_Cookies():
	login = session.get('http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_slogin.html')
	headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
	           'Accept-Encoding': 'gzip, deflate',
	           'Accept-Language': 'zh-CN,zh;q=0.8',
	           'Cache-Control': 'no-cache',
	           'Connection': 'keep-alive',
	           'Cookie': 'JSESSIONID=' + session.cookies.values()[0],
	           'DNT': '1',
	           'Host': 'jwgl6.ujn.edu.cn',
	           'Proxy-Connection': 'Keep-Alive',
	           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	session.headers = headers
	be = BeautifulSoup(login.content, 'lxml')
	csrftoken = be.find('input', id='csrftoken')['value']
	return csrftoken


def get_js():
	f = open("/home/testproject/polls/base64.js", "r", encoding='utf-8')
	line = f.readline()
	htmlstr = ''
	while line:
		htmlstr = htmlstr + line
		line = f.readline()
	f.close()
	return htmlstr


def getPublicKey():
	fir = int(time.time() * 1000)
	time.sleep(random.random())
	sec = int(time.time() * 1000)
	publickey = session.get(
		'http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(sec) + '&_=' + str(fir))
	pk = json.loads(publickey.content.decode('utf-8'))
	return pk


def encryptPwd(m, e):
	ctx = execjs.compile(get_js())
	m = int(ctx.call('b64tohex', m), 16)
	e = int(ctx.call('b64tohex', e), 16)
	publickey = rsa.PublicKey(m, e)
	password = rsa.encrypt(bytes(pwd, 'utf-8'), publickey)
	password = binascii.b2a_hex(password)
	password = ctx.call('hex2b64', str(password, 'utf-8'))
	return password


def login(csrftoken, username, password):
	data = {'csrftoken': csrftoken, 'yhm': username, 'mm': password, 'mm': password}
	session.post('http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_slogin.html', data=data)
	saveCookies(session.cookies)


# session.get('http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_slogin.html')
# session.get('http://jwgl6.ujn.edu.cn/jwglxt/xtgl/index_initMenu.html?jsdm=xs&_t=' + str(int(time.time() * 1000)))
def getCj(xn, xq):
	query_data = {'xnm': xn, 'xqm': xq, '_search': 'false', 'nd': str(int(time.time() * 1000)),
	              'queryModel.showCount': 20, 'queryModel.currentPage': 1, 'queryModel.sortName': '',
	              'queryModel.sortOrder': 'asc', 'time': 0}
	res = session.post('http://jwgl6.ujn.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005',
	                   data=query_data)
	txt = json.loads(res.content.decode('utf-8'))
	for i in txt['items']:
		yield '课程名称 : ' + i['kcmc'] + '\n' + '成绩 : ' + i['cj'] + '\n\n'


def checkCookies():
	res = session.get('http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_slogin.html')
	if res.url.__contains__('index'):
		return True
	else:
		return False
def noCookiesLogin():
	csrftoken = getcsrftoken_Cookies()
	publickeydict = getPublicKey()
	m = publickeydict['modulus']
	e = publickeydict['exponent']
	password = encryptPwd(m, e)
	login(csrftoken, username, password)
def wx(xn, xq):
	list=''
	if (os.path.exists('/home/testproject/polls/cookies.txt')):
		session.cookies=getCookies()
		if not checkCookies():
			noCookiesLogin()
	else:
		noCookiesLogin()
	for i in getCj(xn, xq):
		list += i
	return list

if __name__ == '__main__':
	print(wx(2016, 12))