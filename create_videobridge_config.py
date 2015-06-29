#!/usr/bin/python
"""
	create_videobridge_config:
	This script creates the following configuration file that will be 
	read  by JItsi Videobridge component, at startup

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os

def create_videobridge_config(prosody_section, jicofo_section):
	
	print "config file path is %s" %jicofo_section['config_file_path']
	jicofo_config_file = open(os.path.join(jicofo_section['config_file_path'], "config"),'w')
	# create the lines 
	line1 = "# Jitsi Videobridge settings\n"
	line2 = "JVB_HOST=localhost\n"
	line3 = "JVB_HOSTNAME=" + prosody_section['domain'] + "\n"
	line4 = "JVB_SECRET=fO@OAfyH\n"
	line5 = "JVB_PORT=5347\n"
	line6 = "JVB_OPTS=\"\"\n"
	
	# write all the lines to the file
	jicofo_config_file.write("%s%s%s%s%s%s" % (line1, line2, line3, line4, line5, line6))
	
	jicofo_config_file.close()
	return True
		
if __name__ == '__main__':
		cpc = create_videobridge_config(sys.argv[1])