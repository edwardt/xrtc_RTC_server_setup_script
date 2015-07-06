#!/usr/bin/python
"""
	create_jicofo_config:
	This script creates the configuration file that will be 
	read  by JICOFO component, at startup

	requires:
		- Python 2.6+
		- Linux 2.6.x

"""

import sys, os, re

def create_jicofo_config(prosody_section, jicofo_section):
	
	print "config file path is %s" %jicofo_section['config_file_path']
	jicofo_config_file = open(os.path.join(jicofo_section['config_file_path'], "config"),'w')
	domain =  prosody_section['domain']
	
	# create the lines 
	line1 = "# Jitsi Conference Focus settings\n"
	line2 = "JICOFO_HOST=localhost\n"
	line3 = "JICOFO_HOSTNAME=" + domain + "\n"
	line4 = "JICOFO_SECRET=Xtjn@I1#\n"
	line5 = "JICOFO_PORT=5347\n"
	line6 = "JICOFO_AUTH_DOMAIN=auth." + domain + "\n"
	subdomain = prosody_section['focus_fqdn'].split(".")[0]
	# register an account with "subdomain" as the user and "JICOFO_SECRET" as the password
	register_string = "prosodyctl register " + subdomain + " auth." + domain + " Xtjn@I1#"
	os.system(register_string)
	
	# determine if domain is IPv4 or IPv6 address.
	# check if domain contains numbers and '.' only
	if re.match("^[\d.]*$", domain):
		line7 = ""
	else:
		line7 = "JICOFO_SUBDOMAIN=" + subdomain + "\n"
	line8 = "JICOFO_AUTH_USER=xrtc_sp00f_f0cus\nJICOFO_AUTH_PASSWORD=xrtc_sp00f_f0cus\nJICOFO_OPTS=\"\"\n"
	
	# write all the lines to the file
	jicofo_config_file.write("%s%s%s%s%s%s%s%s" % (line1, line2, line3, line4, line5, line6, line7, line8))
	
	jicofo_config_file.close()
	return True
		
if __name__ == '__main__':
		cpc = create_jicofo_config(sys.argv[1])