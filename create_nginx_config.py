#!/usr/bin/python
"""
	create_nginx_config:
	This script creates the configuration file that nginx service will read, at startup

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys, os

def create_nginx_config(prosody_section, nginx_section):
	
	print "config file path is %s" %nginx_section['config_file_path']
	nginx_config_file = open(os.path.join(nginx_section['config_file_path'], nginx_section.get('config_file_name')),'w')
	xmpp_fqdn = prosody_section['xmpp_fqdn']
	# create the lines 
	line1 = "server {\n\tlisten 80;\n\t"
	# if SSL_KEY and SSL_CERt exists listen on port 443
	ssl_key = nginx_section.get('ssl_key', None)
	ssl_cert = nginx_section.get('ssl_cert', None)
	if os.path.isfile(ssl_key) and os.path.isfile(ssl_cert):
		line2 = "listen 443 ssl;\n\t"
	else:
		line2 = "\n\t"
	line3 = "server_name " + xmpp_fqdn + ";\n\t"
	line4 = "location ~ ^/([a-zA-Z0-9=\?]+)$ {\n\t\trewrite ^/(.*)$ / break;\n\t}\n\t"
	line5 = "location /http-bind {\n\t\tproxy_pass http://localhost:5280/http-bind;\n\t\tproxy_set_header X-Forwarded-For $remote_addr;\n\t\tadd_header 'Access-Control-Allow-Origin' \"$http_origin\";\n\t}\n\t"
	line6 = "# xmpp websockets"
	line7 = "location /xmpp-websocket {\n\t\tproxy_pass http://localhost:5280;\n\t\tproxy_set_header X-Forwarded-For $remote_addr;\n\t\tproxy_http_version 1.1;\n\t\tproxy_set_header Upgrade $http_upgrade;\n\t\tproxy_set_header Connection \"upgrade\";\n\t\ttcp_nodelay on;\n\t\tproxy_read_timeout 300s;\n\t}\n}\n"
	
	line8 = "server {\n\tlisten [::]:80;\n\t"
	# if SSL_KEY and SSL_CERt exists listen on port 443
	if os.path.isfile(ssl_key) and os.path.isfile(ssl_cert):
		line9 = "listen [::]:443 ssl;\n\t"
	else:
		line9 = "\n\t"
	line10 = "server_name " + xmpp_fqdn + ";\n\t"
	line11 = "location ~ ^/([a-zA-Z0-9=\?]+)$ {\n\t\trewrite ^/(.*)$ / break;\n\t}\n\t"
	line12 = "location /http-bind {\n\t\tproxy_pass http://localhost:5280/http-bind;\n\t\tproxy_set_header X-Forwarded-For $remote_addr;\n\t\tadd_header 'Access-Control-Allow-Origin' \"$http_origin\";\n\t}\n\t"
	line13 = "# xmpp websockets"
	line14 = "location /xmpp-websocket {\n\t\tproxy_pass http://localhost:5280;\n\t\tproxy_set_header X-Forwarded-For $remote_addr;\n\t\tproxy_http_version 1.1;\n\t\tproxy_set_header Upgrade $http_upgrade;\n\t\tproxy_set_header Connection \"upgrade\";\n\t\ttcp_nodelay on;\n\t\tproxy_read_timeout 300s;\n\t}\n}\n"
	
	# write all the lines to the file
	nginx_config_file.write("%s%s%s%s%s" % (line1, line2, line3, line4, line5))
	nginx_config_file.write("%s%s%s%s%s" % (line6, line7, line8, line9, line10))
	nginx_config_file.write("%s%s%s%s" % (line11, line12, line13, line14))
	
	nginx_config_file.close()
	return True
		
if __name__ == '__main__':
		cpc = create_nginx_config(sys.argv[1])
		