"""
	base_config_reader:
		This file parses a config file containing configuration parameters

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import os, ConfigParser, sys

def validate_config_file_path(section):
	path = section.get('config_file_path', None)
	if not os.path.isdir(path):
		print "config_file_path key not present or config_file_path has no value or config_file_path does not exist"
		return False
	return True

 
class BaseConfigReader(ConfigParser.ConfigParser):
	# constructor
	def __init__(self, conffile):
		try: 
			ConfigParser.ConfigParser.__init__(self)
			self.read(conffile)
			self.d = {}
		except IOError as Err:
			raise Err

	def get_dict(self):
		self.d = dict(self._sections)
		for k in self.d:
			# creates a dictionary based on _defaults OrderedDict()
			# **d[k], it means that d[k] (dictionary) is decomposed into assignments.
			# This is necessary as the dict() method requires assignments as additional
			#  parameters to the method.
			self.d[k] = dict(self._defaults, **self.d[k])
			# if the key is in the dictionary, remove it and return its value.
			# Otherwise, return default which is None. If no default is specified
			# and the key is not in the dictionary, an exception (KeyError) is
			# raised.
			self.d[k].pop('__name__', None)
		return self.d

	def validate_prosody_section(self):
		prosody_section = self.d.get('PROSODY')
		domain = self.validate_domain(prosody_section)
		if not domain:
			return False
		if not self.validate_fqdn(prosody_section, domain, 'conference_fqdn'):
			return False
		if not self.validate_fqdn(prosody_section, domain, 'xmpp_fqdn'):
			return False
		if not self.validate_fqdn(prosody_section, domain, 'focus_fqdn'):
			return False
		if not self.validate_fqdn(prosody_section, domain, 'jirecon_fqdn'):
			return False
		if not self.validate_fqdn(prosody_section, domain, 'callcontrol_fqdn'):
			return False
		if not self.validate_s2s(prosody_section):
			return False
		if not self.validate_token_authentication(prosody_section):
			return False
		if not self.validate_cassandra_db(prosody_section):
			return False
		if not validate_config_file_path(prosody_section):
			return False
		return True
	
	def validate_domain(self, prosody_section):
		domain = prosody_section.get('domain', None)
		if not domain:
			return None
		return domain
		
	def validate_fqdn(self, prosody_section, domain, key):
		fqdn = prosody_section.get(key, None)
		if not fqdn:
			print "%s key not present or has no value" %key
			return False
		else:
			if domain not in fqdn:
				print "Invalid key %s" %fqdn
				return False
		return True
		
	def validate_s2s(self, prosody_section):
		s2s = prosody_section.get('s2s', None)
		if s2s is None:
			print "S2S key not present or has no value"
			return False
		elif s2s == 'true':
			ssl_key = prosody_section.get('ssl_key', None)
			if not ssl_key:
				print "SSL_KEY key not present or has no value"
				return False
			else:
				ssl_cert = prosody_section.get('ssl_cert', None)
				if not ssl_cert:
					print "SSL_CERT key not present or has no value"
					return False
		return True
		
	def validate_token_authentication(self, prosody_section):
		token_auth = prosody_section.get('token_authentication', None)
		if token_auth is None:
			print "TOKEN_AUTHENTICATION key not present or has no value"
			return False
		return True
		
	def validate_cassandra_db(self, prosody_section):
		cassandra_db = prosody_section.get('cassandra_db', None)
		if cassandra_db is None or cassandra_db == "":
			print "CASSANDRA_DB key not present or has no value"
			return False
		return True
		
	def validate_jicofo_section(self):
		jicofo_section = self.d.get('JICOFO')
		if not validate_config_file_path(jicofo_section):
			return False
		return True
		
	def validate_jvb_section(self):
		jvb_section = self.d.get('JVB')
		if not validate_config_file_path(jvb_section):
			return False
		return True

			

if __name__ == "__main__":
	bcr = BaseConfigReader(os.path.join(os.getcwd(), "config.ini"))
	d = bcr.get_dict()
	prosody_status = bcr.validate_prosody_section()
	if not prosody_status:
		sys.exit("Invalid prosody base config. exiting...")
	jicofo_status = bcr.validate_jicofo_section()
	if not jicofo_status:
		sys.exit("Invalid jicofo base config. exiting...")
	jvb_status = bcr.validate_jvb_section()
	if not jvb_status:
		sys.exit("Invalid jvb base config. exiting...")
	
	