#!/usr/bin/python
#common gateway interface
import cgi
import cgitb
import mysql.connector as mariadb
import commands
import time
cgitb.enable()
print"content-type:text/html"
print ""
form=cgi.FieldStorage()#form is a variable
#username="naveen"store value whose name is rahul
commands.getstatusoutput("systemctl restart mariadb")
mariadb_connection = mariadb.connect(user='root', password='redhat', database='cloud')
cursor = mariadb_connection.cursor()
namesoft=form.getvalue('saas')
cc=form.getvalue('cook')
username=cc[8:len(cc)]
print namesoft+"\n"
passkey='select * from clients where username="'+username+'"'
cursor.execute(passkey)
r=cursor.fetchall()
print r
for i in r:
    password=str(i[2])
print password
username=username+"saas"
print username
print password
commands.getstatusoutput("sudo -i useradd "+username)
commands.getstatusoutput("sudo -i echo -e '"+password+"\\n"+password+"' | sudo -i  passwd "+username)
fh=open("/var/www/html/"+username+"/saas.py",mode="w")
commands.getstatusoutput("sudo -i chmod +x /var/www/html/"+username+"/saas.py")
b='#!/usr/bin/python2\nimport commands\ncommands.getstatusoutput("ssh -X '+username+'@192.168.0.7 '+namesoft+'")'
fh.write(b)
fh.close()	
b=commands.getstatusoutput("sudo -i tar -cf saas.tar  --directory='/var/www/html/"+username+"' saas.py;sudo -i mv saas.tar /var/www/html/")
print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=http://192.168.0.7/saas.tar\">\n";
print b[0]
print b
mariadb_connection.close()
