#!/usr/bin/python
"""
	create_rtc_config_files:
	This script creates the following configuration files
		- /etc/prosody/conf.d/component.cfg.lua
		- /etc/jitsi/jicofo/config
		- /etc/jitsi/jitsi-videobridge/config

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import sys
from base_config_reader import BaseConfigReader
from create_nginx_config import create_nginx_config
from create_prosody_config import create_prosody_config
from create_jicofo_config import create_jicofo_config
from create_videobridge_config import create_videobridge_config
from create_jirecon_config import create_jirecon_config

class CreateRtcConfigFiles:
	# constructor
	def __init__(self, config_file):
		self.bcr = BaseConfigReader(config_file)
		self.d = {}
		
	# main run method
	# single threaded periodic timer implementation
	def run(self):
		self.d = self.bcr.get_dict()
		
		# validate base config 
		nginx_section_status = self.bcr.validate_nginx_section()
		if not nginx_section_status:
			sys.exit("Invalid nginx section. exiting...")
		prosody_section_status = self.bcr.validate_prosody_section()
		if not prosody_section_status:
			sys.exit("Invalid prosody section. exiting...")
		jicofo_section_status = self.bcr.validate_jicofo_section()
		if not jicofo_section_status:
			sys.exit("Invalid jicofo section. exiting...")
		jvb_section_status = self.bcr.validate_jvb_section()
		if not jvb_section_status:
			sys.exit("Invalid jvb section. exiting...")
		#jirecon_section_status = self.bcr.validate_jirecon_section()
		#if not jirecon_section_status:
			#sys.exit("Invalid jirecon section. exiting...")
			
		# generate config files
		nginx_config_status = create_nginx_config(self.d['PROSODY'], self.d['NGINX'])
		if not nginx_config_status:
			sys.exit("nginx config file not created. Exiting ...")
		prosody_config_status = create_prosody_config(self.d['PROSODY'], self.d['NGINX'])
		if not prosody_config_status:
			sys.exit("prosody config file not created. Exiting ...")
		jicofo_config_status = create_jicofo_config(self.d['PROSODY'], self.d['JICOFO'])
		if not jicofo_config_status:
			sys.exit("jicofo config file not created. Exiting ...")
		videobridge_config_status = create_videobridge_config(self.d['PROSODY'], self.d['JVB'])
		if not videobridge_config_status:
			sys.exit("videobridge config file not created. Exiting ...")
		#jirecon_config_status = create_jirecon_config(self.d['PROSODY'], self.d['JIRECON'])
		#if not jirecon_config_status:
			#sys.exit("jirecon config file not created. Exiting ...")
		
if __name__ == '__main__':
	try:
		crcf = CreateRtcConfigFiles(sys.argv[1])	# instantiate class
	except ConfigParser.MissingSectionHeaderError:
		sys.exit("%s does not start with section header. exiting..." %sys.argv[1])
	# moving on
	crcf.run()
