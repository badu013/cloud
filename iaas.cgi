#!/usr/bin/python2
#common gateway interface
import cgi
import commands
import cgitb
import random
import string
import mysql.connector as mariadb
#cgitb=traceback
cgitb.enable()
#content type text and html
print "content-type:text/html"
print""
form=cgi.FieldStorage()
os=form.getvalue('os')
#form is used to store data taken from form
ccpu=form.getvalue('vcpu')
store=form.getvalue('vcpu1')
ram=form.getvalue('vcpu2')
cc=form.getvalue('cook')
username=cc[8:len(cc)]
print os
print ccpu
print store
print ram
print cc
print cc[8:len(cc)]
commands.getstatusoutput("sudo -i systemctl restart mariadb")
ms=mariadb.connect(user='root',password='redhat',database='cloud')
cursor=ms.cursor()
a=""
b=""
if os==str(1):
	a="projos"#name of orignal os
	#s="projosA"name of qcow file of new os
	b="Redhat7"
elif os==str(2):
	a="projoswin"
	b="FEDORA"
else:
	a="projos"
	b="Redhat7"
cursor.execute("select "+b+" from clients where username='"+username+"'")
r=cursor.fetchall()
print r
for i in r:
    countos=str(i[0])
print "oscount "+countos

cos=int(countos)
cos=cos+1
print "\n"+str(cos)
s="projos"+str(cos)
cursor.execute("update clients set "+b+"="+str(cos)+" where username='"+username+"'")
ms.commit();
ms.close();
print a+"\n"
print s+"\n"
print b+"\n"
x=commands.getstatusoutput("sudo -i cp /etc/libvirt/qemu/"+a+".xml /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
st=commands.getstatusoutput("sudo -i grep -w \"<uuid\" /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
uuid=st[1].strip()[6:42]
nuuid=uuid.replace(uuid[random.randint(0,4)],str(random.randint(1,9)))
#nuuid=nuuid.replace(uuid[random.randint(30,33)],str(random.randint(1,9)))
x=commands.getstatusoutput("sudo -i sed -i 's/"+uuid+"/"+nuuid+"/' /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
st=commands.getstatusoutput("sudo -i grep -w \"<mac\" /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
mac=st[1].strip()[14:31]
print st
print mac
nmac=mac.replace(mac[random.randint(0,1)],str(random.randint(1,9)))
nmac=mac.replace(mac[random.randint(3,4)],str(random.randint(1,9)))
print nmac
y=commands.getstatusoutput("sudo sed -i 's/"+mac+"/"+nmac+"/' /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
print y
por=random.randint(5905,5999)
x=commands.getstatusoutput("sudo -i sed -i 's/5900/"+str(por)+"/' /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
x=commands.getstatusoutput("sudo -i sed -i 's/"+a+"/"+a+"_"+username+"_"+str(cos)+"/' /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
x=commands.getstatusoutput("sudo -i sed -i 's/"+a+"_"+username+"_"+str(cos)+".qcow2/"+s+".qcow2/' /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
x=commands.getstatusoutput("sudo -i replace 'linux_cloud'  'linux_cloud/"+username+"' -- /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
x=commands.getstatusoutput("sudo -i virsh define /etc/libvirt/qemu/"+a+"_"+username+"_"+str(cos)+".xml")
x=commands.getstatusoutput("sudo -i virsh start "+a+"_"+username+"_"+str(cos))
proxyport=random.randint(9000,9999)
x=commands.getstatusoutput("/software/websockify-master/websockify.py "+str(proxyport)+" 192.168.0.7:"+str(por)+" -D")
#commands.getstatusoutput("sudo -i mkdir /var/www/html/linux_cloud_proj/"+username)
#commands.getstatusoutput("sudo -i chmod +777 /var/www/html/linux_cloud_proj/"+username)
fname=username+""+str(cos)
fh=open("/var/www/html/linux_cloud_proj/"+fname+".txt",mode="w")
commands.getstatusoutput("sudo -i chmod 644 /var/www/html/linux_cloud_proj/"+fname+".txt")
ifname='<iframe class="icss'+str(cos)+' id="ss" style="position:absolute" src="http://192.168.0.7/vnc/?host=192.168.0.7&port='+str(proxyport)+'"></iframe><br>'
fh.write(ifname)
fh.close()
"""
osfile=username+"_oscur.txt"
fos=open("/var/www/html/linux_cloud_proj/"+osfile+"_oscur.txt",mode="w")
commands.getstatusoutput("sudo -i chmod 644 /var/www/html/linux_cloud_proj/"+osfile+".txt")
fos.write(str(cos))
fos.close()
"""
print "Set-Cookie:rcookie="+username+","+str(cos)+";Path=/;\r\n" 
#print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=http://192.168.0.7/vnc/?host=192.168.0.7&port="+str(proxyport)+"\">\n";
print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=http://192.168.0.7/linux_cloud_proj/home.php\">\n";
#print "out is "+str(x[0])
print os+"\n"
print "\n"+hello
print "\n"+he
print "\n"+hey
#store value whose name rahul 
#
