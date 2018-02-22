import re
import polls.fuckujn
from django.http import HttpResponse
import time
import json

# Create your views her.
lastcreatetime=0
result=''
def index(request):
	if request.method == 'POST':
		xmldata = str(request.read(), 'utf-8')
		textpat = re.compile(r'CDATA\[\w*\]')
		intpat = re.compile(r'<CreateTime>\d*</CreateTime>')
		body = textpat.findall(xmldata)
		createtime = intpat.findall(xmldata)
		global lastcreatetime
		print(createtime[0][12:-13]==lastcreatetime)
		if(createtime[0][12:-13]!=lastcreatetime):
			print(lastcreatetime)
			lastcreatetime=createtime[0][12:-13]
			touser = body[0][6:-1]
			fromuser = body[1][6:-1]
			content = xmldata[xmldata.index('<Content><') + 18:xmldata.index('></Content>') - 2]
			global result
			if content =='结果':
				content=result
			if content .__contains__('查询'):
				xn=content[2:6]
				xq=content[6:]
				result = polls.fuckujn.wx(int(xn), int(xq))
				content=result
			print(content)
				# for i in cj:
				#    content+=i
			ttt = '<xml>' \
			      '<ToUserName><![CDATA[' + fromuser + ']]></ToUserName>' \
			                                           '<FromUserName><![CDATA[' + touser + ']]></FromUserName>' \
			                                                                                '<CreateTime>' + str(
				int(time.time())) + '</CreateTime>' \
			                        '<MsgType><![CDATA[text]]></MsgType>' \
			                        '<Content><![CDATA[' + content + ']]></Content></xml>'
			print(ttt)
			return HttpResponse(ttt)
		else:
			return HttpResponse('')
	elif request.method == 'GET':
		echostr = request.GET.get('echostr')
		return HttpResponse(echostr)
