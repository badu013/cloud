#!/usr/bin/python
#common gateway interface
import cgi
import cgitb
import mysql.connector as mariadb
import commands
cgitb.enable()
print"content-type:text/html"
print ""
form=cgi.FieldStorage()#form is a variable
#username="manav" store value whose name is rahul
commands.getstatusoutput("systemctl restart mariadb")
mariadb_connection = mariadb.connect(user='root', password='redhat', database='cloud')
cursor = mariadb_connection.cursor()
hello=form.getvalue('slsize')
he=form.getvalue('proto')
cc=form.getvalue('cook')
username=cc[8:len(cc)]
print he
print hello
print username
passkey='select * from clients where username="'+username+'"'
cursor.execute(passkey)
r=cursor.fetchall()
print r
for i in r:
    password=str(i[2])
    usernamen=str(i[0])
    print password
    print usernamen
print usernamen
commands.getstatusoutput("sudo -i mkdir /var/www/html/"+usernamen)
commands.getstatusoutput("sudo -i mkdir /clientpy/" + usernamen)
commands.getstatusoutput("sudo -i chmod 755 /clientpy/" + usernamen)
if he=="nfs":
	commands.getstatusoutput("sudo -i lvcreate --size " + str(hello) + "G --name " + usernamen + " thunder")
	commands.getstatusoutput("sudo -i mkfs.ext4 /dev/thunder/" + usernamen)
	commands.getstatusoutput("sudo -i mkdir /storage/" + usernamen)
	commands.getstatusoutput("sudo -i chmod 755 /storage/" +usernamen)
	commands.getstatusoutput("sudo -i mount /dev/thunder/" + usernamen + " /storage/"+usernamen)
	commands.getstatusoutput("sudo -i chmod 777 /etc/exports")
	a="/storage/" + usernamen + " *(rw,no_root_squash)" + "\n"
	fh=open("/etc/exports", mode="w")
	fh.write(a)
	fh.close()
	commands.getstatusoutput("sudo -i systemctl restart nfs-server")
	commands.getstatusoutput("sudo  touch /clientpy/"+usernamen+"/nfsclient.py")
	commands.getstatusoutput("sudo -i chmod 777 /clientpy/"+usernamen+"/nfsclient.py")
	b='#!/usr/bin/python2\nimport commands\ncommands.getstatusoutput("mkdir /media/'+usernamen+'")\ncommands.getstatusoutput("mount 192.168.0.7:/storage/' + usernamen + ' /media/'+usernamen+'")\n'
	commands.getstatusoutput("sudo -i chmod 777 /clientpy/"+usernamen+"/nfsclient.py")
	fs=open('/clientpy/'+usernamen+'/nfsclient.py',mode="w")	
	fs.write(b)
	fs.close()
	commands.getstatusoutput("sudo -i systemctl restart nfs-server")
	commands.getstatusoutput("sudo -i chmod +x /clientpy/"+usernamen+"/nfsclient.py")
	
	#commands.getstatusoutput("mkdir /root/var/www/"+username)
	commands.getstatusoutput("sudo -i tar -cvf /var/www/html/"+usernamen+"/nfsclient.tar  /clientpy/"+usernamen+"/nfsclient.py")
	
	print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=http://localhost/"+usernamen+"/nfsclient.tar\">\n";

elif he=="smb":
	#commands.getstatusoutput("mkdir"+ username)
	commands.getstatusoutput("sudo -i useradd -s /sbin/nologin "+usernamen)
	commands.getstatusoutput("sudo echo -e '"+password+"\\n"+password+"'|sudo smbpasswd -a "+ usernamen)
	commands.getstatusoutput("sudo -i mkdir /samba")
	commands.getstatusoutput("sudo -i mkdir /samba/"+usernamen)
	commands.getstatusoutput("sudo -i chmod o+w /samba/"+usernamen)
	
	commands.getstatusoutput("sudo -i lvcreate --size " + str(hello) + "G --name "+usernamen+"1 thunder")
	commands.getstatusoutput("sudo -i mkfs.ext4 /dev/thunder/" + usernamen+"1")
	#commands.getstatusoutput("sudo -i mkdir /storage/" + usernamen)
	commands.getstatusoutput("sudo -i mount /dev/thunder/"+usernamen+"1 /samba/"+usernamen)
	a="[docs"+usernamen+"]\npath=/samba/"+usernamen+"\nwritable=yes\nvalid users="+usernamen+"\nbrowseable=yes\n"
	commands.getstatusoutput("sudo -i chmod o+w /etc/samba/smb.conf")
	fh=open("/etc/samba/smb.conf", mode="w")
	fh.write(a)
	fh.close()
	commands.getstatusoutput("sudo -i systemctl restart smb")
	commands.getstatusoutput("sudo -i mkdir /"+usernamen)
	commands.getstatusoutput("sudo -i chmod o+w /"+usernamen)
	commands.getstatusoutput("sudo -i touch /"+usernamen+"/sambaclient.py")
	commands.getstatusoutput("sudo -i chmod o+w /"+usernamen+"/sambaclient.py")
	
	b='#!/usr/bin/python2\nimport commands\ncommands.getstatusoutput("mkdir /media/samba")\ncommands.getstatusoutput("mkdir /media/samba/'+usernamen+'")\ncommands.getstatusoutput("mount -o username='+usernamen+' //192.168.0.7/docs'+usernamen+' /media/samba/'+usernamen+'")'
	#commands.getstatusoutput("chmod o+w /media/samba/"+usernamen+"/sambaclient.py")
	

	fh=open("/"+usernamen+"/sambaclient.py",mode="w")
	fh.write(b)
	fh.close()
	commands.getstatusoutput("sudo -i chmod +x /"+usernamen+"/sambaclient.py")
	#commands.getstatusoutput("mkdir /root/var/www/"+username)
	commands.getstatusoutput("sudo -i tar -cvf /var/www/html/"+usernamen+"/sambaclient.tar /"+usernamen+"/sambaclient.py")

	commands.getstatusoutput("sudo -i systemctl restart smb")
	mariadb_connection.close()
	print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=http://localhost/"+usernamen+"/sambaclient.tar\">\n";
	
	#print "<META HTTP-EQUIV=REFRESH CONTENT=\"0;URL=localhost/"+usernamen+"sambaclient.tar\">\n";
"""
elif he=="gluster":
	commands.getstatusoutput("sudo -i mkdir /gluster")
	commnads.getstatusoutput("sudo -i chmod o+w /gluster")
	commands.getstatusoutput("sudo -i mkdir /gluster"+usernamen)
	commands.getstatusoutput("sudo -i chmod o+w /gluster/"+usernamen)
	commands.getstatusoutput("sudo -i lvcreate --size " + str(hello) + "G --name "+usernamen+"gfs thunder")
	commands.getstatusoutput("sudo -i mkfs.ext4 /dev/thunder/" + usernamen+"gfs")
	commands.getstatusoutput("sudo -i lvcreate --size " + str(hello) + "G --name "+usernamen+"gfs1 thunder")
	commands.getstatusoutput("sudo -i mkfs.ext4 /dev/thunder/" + usernamen+"gfs1")
	commands.getstatusoutput("sudo -i mount /dev/thunder/"+usernamen+"gfs /gluster/"+usernamen)
	commands.getstatusoutput("sudo -i mount /dev/thunder/"+usernamen+"gfs1 /gluster/"+usernamen)
	commands.getstatusoutput("sudo -i systemctl restart glusterd")
	commands.getstatusoutput("sudo -i gluster volume create glusterstorage"+usernamen" 192.168.0.7:/thunder/"+usernamen+"gfs 192.168.0.7:/thunder/"+usernamen+"gfs1 force")
	commands.getstatusoutput("sudo -i gluster volume start glusterstorage"+usernamen)
	commands.getstatusoutput("sudo -i mkdir /"+usernamen+"gfs")
	commands.getstatusoutput("sudo -i chmod o+w /"+usernamen+"gfs")
	commands.getstatusoutput("sudo -i touch /"+usernamen+"gfs/gfsclient.py")
	commands.getstatusoutput("sudo -i chmod o+w /"+usernamen+"/gfsclient.py")
	a='#!/usr/bin/python2\nimport commands\ncommands.getstatusoutput("sudo -i mkdir /media/'+usernamen+'gfs")\ncommands.getstatusoutput("sudo -i mount -t glusterfs 192.168.0.7:/glusterstorage'+usernamen+' /media/'+usernamen+'gfs")'
	fh=open("/"+usernamen+"gfs/gfsclient.py",mode="at")
	fh.write(a)
	fh.close(a)
	commands.getstatusoutput("sudo -i chmod +x /"+usernamen+"gfs/gfsclient.py")
	
"""	
	
	
			

