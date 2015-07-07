#!/usr/bin/python
"""
	create_prosody_config:
	This script creates the following configuration file that will be 
	included as an extention to /etc/prosody/prosody.cfg.lua

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os, stat, shutil

def create_prosody_config(prosody_section, nginx_section):
	if not os.path.isfile("/etc/prosody/prosody.cfg.lua"):
		print "copying /etc/prosody/prosody.cfg.lua.default to /etc/prosody/prosody.cfg.lua"
		shutil.copy("/etc/prosody/prosody.cfg.lua.default", "/etc/prosody/prosody.cfg.lua")
		
	print "config file path is %s" %prosody_section['config_file_path']
	component_cfg_lua_file = open(os.path.join(prosody_section['config_file_path'], "component.cfg.lua"),'w')
	domain = prosody_section['domain']
	# create the lines 
	line1 = "admins = {\"jitsi-videobridge." + domain + ",xrtc_sp00f_f0cus@auth." + domain +"\"}\n"
	line2 = "s2s_secure_auth = " + prosody_section['s2s'] + "\n"
	s2s = prosody_section.get('s2s', None)
	if s2s and s2s == 'true':
		line3 = "ssl = {" + "\n\tkey = \"" + nginx_section['ssl_key'] + "\";\n\tcertificate = \"" + nginx_section['ssl_cert'] + "\";\n}\n"
	else:
		line3 = "\n"
	line4 = "token_authentication = \""+ prosody_section['token_authentication'] + "\"\n"
	if domain != prosody_section['xmpp_fqdn']:
		line5 = "VirtualHost \"" + domain + "\"\n\tauthentication = \"internal_plain\"\n"
	else:
		line5 = "\n"
	
	line6 = "VirtualHost \"auth." + domain + "\"\n\tauthentication = \"internal_plain\"\n"
	line7 = "VirtualHost \"" + prosody_section['xmpp_fqdn'] + "\"\n\tauthentication = \"internal_plain\"\n" \
					"\thttp_host = {\"localhost\",\"ip6-localhost\"}\n" \
					"\tmodules_enabled = {\n\t\t" \
					"\"bosh\";\n\t\t\"websocket\";\n\t\t\"pubsub\";\n\t\t\"s2s\";\n\t}\n"
	line8 = "Component \"" + prosody_section['conference_fqdn'] + "\" \"muc\"\n\t" \
					"modules_enabled = {\n\t\t\"mam_rest\";\n\t}\n\tstorage = {\n\t\tarchive2 = \"cassandra\"\n\t}\n\t" \
					"cassandra = {host = \"" +  prosody_section['cassandra_db'] + "\"}\n"
	line9 = "Component \"jitsi-videobridge." + domain + "\"\n\t component_secret = \"fO@OAfyH\"\n"
	line10 = "Component \"" + prosody_section['focus_fqdn'] + "\"\n\t component_secret = \"Xtjn@I1#\"\n"
	#if prosody_section['jirecon_fqdn']:
		#line11 = "Component \"" + prosody_section['jirecon_fqdn'] + "\"\n\t component_secret = \"record\"\n"
	#else:
		#line11 = "\n"
	
	# write all the lines to the file
	component_cfg_lua_file.write("%s%s%s%s%s" % (line1, line2, line3, line4, line5))
	component_cfg_lua_file.write("%s%s%s%s%s%s" % (line6, line7, line8, line9, line10, line11))
	
	component_cfg_lua_file.close()
	os.chmod(os.path.join(prosody_section['config_file_path'], "component.cfg.lua"), stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
	return True
		
if __name__ == '__main__':
		cpc = create_prosody_config(sys.argv[1])