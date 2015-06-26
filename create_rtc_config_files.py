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
from create_prosody_config import create_prosody_config
from create_jicofo_config import create_jicofo_config
from create_videobridge_config import create_videobridge_config

class CreateRtcConfigFiles:
	# constructor
	def __init__(self, config_file):
		self.bcr = BaseConfigReader(config_file)
		self.d = {}
		
	# main run method
	# single threaded periodic timer implementation
	def run(self):
		self.d = self.bcr.get_dict()
		
		prosody_section_status = self.bcr.validate_prosody_section()
		if not prosody_section_status:
			sys.exit("exiting without creating files /etc/prosody/conf.d/component.cfg.lua, /etc/jitsi/jicofo/config and /etc/jitsi/jitsi-videobridge/config..")
		prosody_config_status = create_prosody_config(self.d['PROSODY'])
		if not prosody_config_status:
			sys.exit("Invalid prosody config file path. exiting ...")
		jicofo_config_status = create_jicofo_config(self.d['PROSODY'], self.d['JICOFO'])
		if not jicofo_config_status:
			sys.exit("Invalid Jicofo config file path. exiting ...")
		videobridge_config_status = create_videobridge_config(self.d['PROSODY'], self.d['JVB'])
		if not videobridge_config_status:
			sys.exit("Invalid Jitsi-Videobridge config file path. exiting ...")

		
if __name__ == '__main__':
		crcf = CreateRtcConfigFiles(sys.argv[1])	# instantiate class
		crcf.run()
