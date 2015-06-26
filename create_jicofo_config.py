#!/usr/bin/python
"""
	create_jicofo_config:
	This script creates the following configuration file that will be 
	read  by JICOFO component, at startup

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os

def create_jicofo_config(prosody_section, jicofo_section):
	
	print "config file path is %s" %jicofo_section['config_file_path']
	jicofo_config_file = open(os.path.join(jicofo_section['config_file_path'], "jicofo_config"),'w')
	# create the lines 
	line1 = "# Jitsi Conference Focus settings\n"
	line2 = "JICOFO_HOST=localhost\n"
	line3 = "JICOFO_HOSTNAME=" + prosody_section['domain'] + "\n"
	line4 = "JICOFO_SECRET=Xtjn@I1#\n"
	line5 = "JICOFO_PORT=5347\n"
	line6 = "JICOFO_AUTH_DOMAIN=auth." + prosody_section['domain'] + "\n"
	subdomain = prosody_section['focus_fqdn'].split(".")[0]
	if (subdomain != 'focus'):
		line7 = "JICOFO_SUBDOMAIN=" + subdomain + "\n"
	else:
		line7=""
	line8 = "JICOFO_AUTH_USER=xrtc_sp00f_f0cus\nJICOFO_AUTH_PASSWORD=xrtc_sp00f_f0cus\nJICOFO_OPTS=\"\""
	
	# write all the lines to the file
	jicofo_config_file.write("%s%s%s%s%s%s%s%s" % (line1, line2, line3, line4, line5, line6, line7, line8))
	
	jicofo_config_file.close()
	return True
		
if __name__ == '__main__':
		cpc = create_jicofo_config(sys.argv[1])