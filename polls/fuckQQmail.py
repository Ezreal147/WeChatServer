import smtplib
from email.mime.text import MIMEText

sender='1473421439@qq.com'
password='qgiulpcdygjkhggg'
reciever='1473421439@qq.com'

message=MIMEText('mail test','plain','utf-8')
message['From']='yzj'
message['To']='test'
message['Subject']='mail test'
server=smtplib.SMTP_SSL('smtp.qq.com',465)
server.login(sender,password)
server.sendmail(sender,[reciever],message.as_string())
server.quit()