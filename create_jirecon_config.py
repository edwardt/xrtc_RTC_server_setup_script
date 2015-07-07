#!/usr/bin/python
"""
	create_jirecon_config:
	This script creates the configuration and properties file that will be 
	read  by JIRECON component, at startup

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os

def create_jirecon_config(prosody_section, jirecon_section):
	
	print "config file path is %s" %jirecon_section['config_file_path']
	# create and write to the config file
	jirecon_config_file = open(os.path.join(jirecon_section['config_file_path'], "config"),'w')
	# create the lines 
	line1 = "# Jirecon settings\n"
	line2 = "JIRECON_CONF=/etc/jitsi/jirecon/jirecon.properties\n"
	line3 = "JIRECON_SECRET=record\n"
	line4 = "JIRECON_PORT=5347\n"
	line5 = "JVB_HOSTNAME=" + prosody_section['domain'] + "\n"
	# write all the lines to the file
	jirecon_config_file.write("%s%s%s%s%s" % (line1, line2, line3, line4, line5))
	jirecon_config_file.close()
	os.chmod(os.path.join(jirecon_section['config_file_path'], "config"), stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

	# create and write to the properties file
	jirecon_properties_file = open(os.path.join(jirecon_section['config_file_path'], "jirecon.properties"),'w')
	# create the lines 
	line1 = "org.jitsi.impl.neomedia.transform.dtls.DtlsPacketTransformer.dropUnencryptedPkts=true\n"
	line2 = "org.jitsi.jirecon.JIRECON_NICKNAME=jirecon\n"
	line3 = "org.jitsi.jirecon.MAX_STREAM_PORT=10000\n"
	line4 = "org.jitsi.jirecon.MIN_STREAM_PORT=8000\n"
	line5 = "org.jitsi.jirecon.STAGING_DIR=" + jirecon_section['staging_dir'] + "\n"
	line6 = "org.jitsi.jirecon.OUTPUT_DIR=" + jirecon_section['output_dir'] + "\n"
	line7 = "org.jitsi.jirecon.XMPP_HOST=" + prosody_section['xmpp_fqdn'] + "\n"
	line8 = "org.jitsi.jirecon.XMPP_PORT=5222\n"
	line9 = "org.jitsi.jirecon.XMPP_USER=xrtc_sp00f_r5c\n"
	line10 = "org.jitsi.jirecon.XMPP_PASS=xrtc_sp00f_r5c\n"
	# write all the lines to the file
	jirecon_properties_file.write("%s%s%s%s%s" % (line1, line2, line3, line4, line5))
	jirecon_properties_file.write("%s%s%s%s%s" % (line6, line7, line8, line9, line10))
	jirecon_properties_file.close()
	os.chmod(os.path.join(jirecon_section['config_file_path'], "jirecon.properties"), stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
	return True
		
if __name__ == '__main__':
		cpc = create_jirecon_config(sys.argv[1])