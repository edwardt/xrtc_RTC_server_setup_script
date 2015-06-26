#!/usr/bin/python
"""
	create_prosody_config:
	This script creates the following configuration file that will be 
	included as an extention to /etc/prosody/prosody.cfg.lua

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os

def create_prosody_config(prosody_section):
	
	print "config file path is %s" %prosody_section['config_file_path']
	component_cfg_lua_file = open(os.path.join(prosody_section['config_file_path'], "component.cfg.lua"),'w')
	# create the lines 
	line1 = "admins = {\"jitsi-videobridge." + prosody_section['domain'] + ",xrtc_sp00f_f0cus@auth." + prosody_section['domain'] +"\"}\n"
	line2 = "s2s_secure auth = " + prosody_section['s2s'] + "\n"
	if  prosody_section.get('s2s', None):
		line3 = "ssl = {" + "\n\tkey = \"" + prosody_section['ssl_key'] + "\";\n\tcertificate = \"" + prosody_section['ssl_cert'] + "\";\n}\n"
	else:
		line3 = "\n"
	line4 = "token_authentication = \""+ prosody_section['token_authentication'] + "\"\n"
	line5 = "VirtualHost \"" + prosody_section['domain'] + "\"\n\tauthentication = \"internal_plain\"\n"
	line6 = "VirtualHost \"auth." + prosody_section['domain'] + "\"\n\tauthentication = \"internal_plain\"\n"
	line7 = "VirtualHost \"" + prosody_section['xmpp_fqdn'] + "\"\n\tauthentication = \"internal_plain\"\n" \
					"\thttp_host = {\"localhost\",\"ip6-localhost\"}\n" \
					"\tmodules_enabled = {\n\t\t" \
					"\"bosh\";\n\t\t\"websocket\";\n\t\t\"pubsub\";\n\t\t\"s2s\";\n\t}\n"
	line8 = "Component \"" + prosody_section['conference_fqdn'] + "\" \"muc\"\n\t" \
					"modules_enabled = {\n\t\t\"mam_rest\";\n\t}\n\tstorage = {\n\t\tarchive2 = \"cassandra\"\n\t}\n\t" \
					" cassandra = {host = \"" +  prosody_section['cassandra_db'] + "\"}\n"
	line9 = "Component \"jitsi-videobridge." + prosody_section['domain'] + "\"\n\t component_secret = \"fO@OAfyH\"\n"
	line10 = "Component \"" + prosody_section['focus_fqdn'] + "\"\n\t component_secret = \"Xtjn@I1#\"\n"

	
	# write all the lines to the file
	component_cfg_lua_file.write("%s\n%s\n%s\n%s\n%s\n" % (line1, line2, line3, line4, line5))
	component_cfg_lua_file.write("%s\n%s\n%s\n%s\n%s\n" % (line6, line7, line8, line9, line10))
	
	component_cfg_lua_file.close()
	return True
		
if __name__ == '__main__':
		cpc = create_prosody_config(sys.argv[1])