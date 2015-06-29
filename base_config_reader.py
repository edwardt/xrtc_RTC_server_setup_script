"""
	base_config_reader:
		This file parses a config file containing configuration parameters

	requires:
		- Python 2.7+
		- Linux 2.6.x

"""

import os, ConfigParser, sys

def validate_config_file_path(section):
	"""
		Checks if config_file_path key exists, in a section. If so, checks if it has a value
		Finally, checks if the config file path exists
	"""
	path = section.get('config_file_path', None)
	if not path:
		print "config_file_path key not present or config_file_path has no value"
		return False
	elif not os.path.isdir(path):
		print "%s directory does not exist" %path
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
		"""
			creates a dictionary for each section in the 
			base config file
		"""
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
		
	def validate_fqdn(self, section, domain, key):
		fqdn = section.get(key, None)
		if not fqdn:
			print "%s key not present or has no value" %key
			return False
		else:
			if domain not in fqdn:
				print "Invalid value %s" %fqdn
				return False
		return True
		
	def validate_domain(self, prosody_section):
		domain = prosody_section.get('domain', None)
		if not domain:
			return None
		return domain
		
	def validate_s2s(self, prosody_section):
		s2s = prosody_section.get('s2s', None)
		if s2s is None:
			print "PROSODY section - S2S key not present or has no value"
			return False
		elif s2s == 'true':
			nginx_section = self.d.get('NGINX')
			ssl_key = nginx_section.get('ssl_key', None)
			if not ssl_key or not os.path.isfile(ssl_key):
				print "NGINX section - SSL_KEY key not present or has no value or SSL_KEY file does not exist"
				return False
			else:
				ssl_cert = nginx_section.get('ssl_cert', None)
				if not ssl_cert or not os.path.isfile(ssl_cert):
					print "NGINX section - SSL_CERT key not present or has no value or SSL_CERT file does not exist"
					return False
		return True
		
	def validate_token_authentication(self, prosody_section):
		token_auth = prosody_section.get('token_authentication', None)
		if token_auth is None:
			print "PROSODY section - TOKEN_AUTHENTICATION key not present or has no value"
			return False
		return True
		
	def validate_cassandra_db(self, prosody_section):
		cassandra_db = prosody_section.get('cassandra_db', None)
		if cassandra_db is None or cassandra_db == "":
			print "PROSODY section - CASSANDRA_DB key not present or has no value"
			return False
		return True
		
	def validate_nginx_section(self):
		"""
			Verifies if
			1. nginx section in base config file exists
			2. config file name is set
		"""
		try:
			nginx_section = self.d.get('NGINX')
			if not validate_config_file_path(nginx_section):
				return False
			else:
				if not nginx_section.get('config_file_name', None):
					print "no nginx config file name in base config file"
					return False
			return True
		except:
			print "NGINX section does not exist"
			return False
		
	def validate_prosody_section(self):
		"""
			Verifies if
			1. prosody section in base config file exists
			2. the keys - CONFIG_FILE_PATH, DOMAIN, CONFERENCE_FQDN, XMPP_FQDN,
										FOCUS_FQDN, S2S and TOKEN_AUTHENTICATION have values
			3. S2S key has value = true, then check if NGINX section has values
				 set for keys - SSL_KEY & SSL_CERT
		"""
		try:
			prosody_section = self.d.get('PROSODY')
			#PROSDY section exists
			domain = self.validate_domain(prosody_section)
			if not domain:
				return False
			if not self.validate_fqdn(prosody_section, domain, 'conference_fqdn'):
				return False
			if not self.validate_fqdn(prosody_section, domain, 'xmpp_fqdn'):
				return False
			if not self.validate_fqdn(prosody_section, domain, 'focus_fqdn'):
				return False
			if not self.validate_s2s(prosody_section):
				return False
			if not self.validate_token_authentication(prosody_section):
				return False
			if not validate_config_file_path(prosody_section):
				return False
			if not self.validate_cassandra_db(prosody_section):
				return False
			return True
		except:
			print "PROSODY section does not exist"
			return False
		
	def validate_jicofo_section(self):
		try:
			jicofo_section = self.d.get('JICOFO')
			#JICOFO section exists
			if not validate_config_file_path(jicofo_section):
				return False
			return True
		except:
			print "JICOFO section does not exist"
			return False
			
	def validate_jvb_section(self):
		try:
			jvb_section = self.d.get('JVB')
			#JVB section exists		
			if not validate_config_file_path(jvb_section):
				return False
			return True
		except:
			print "JVB section does not exist"
			return False
		
	def validate_jirecon_section(self):
		"""
			if PROSODY section contains a value for JIRECON_FQDN key then
			JIRECON section must exist with values set for the keys
			CONFIG_FILE_PATH, STAGING_DIR & OUTPUT_DIR
		"""
		prosody_section = self.d.get('PROSODY')
		if self.validate_fqdn(prosody_section, prosody_section.get('domain'), 'jirecon_fqdn'):
			try:
				jirecon_section = self.d.get('JIRECON')
				#JIRECON section exists
				if (validate_config_file_path(jirecon_section) and \
						jirecon_section.get('output_dir', None) and \
						jirecon_section.get('staging_dir', None)):
					return True
				else:
					print "JIRECON[STAGING_DIR], JIRECON[OUTPUT_DIR] & JIRECON[CONFIG_FILE_PATH] : all must exist"
					return False
				return True		#if PROSODY[JIRECON_FQDN] does not exist then it is not an error. The JIRECON config 
											#and properties files will not be created				
			except:
				print "JIRECON section does not exist"
				return False
			

if __name__ == "__main__":
	try:
		bcr = BaseConfigReader(os.path.join(os.getcwd(), sys.argv[1]))
	except ConfigParser.MissingSectionHeaderError:
		sys.exit("%s does not start with section headers. exiting..." %sys.argv[1])
	d = bcr.get_dict()
	nginx_status = bcr.validate_nginx_section()
	if not nginx_status:
		sys.exit("Invalid nginx base config. exiting...")
	prosody_status = bcr.validate_prosody_section()
	if not prosody_status:
		sys.exit("Invalid prosody base config. exiting...")
	jicofo_status = bcr.validate_jicofo_section()
	if not jicofo_status:
		sys.exit("Invalid jicofo base config. exiting...")
	jvb_status = bcr.validate_jvb_section()
	if not jvb_status:
		sys.exit("Invalid jvb base config. exiting...")
	jirecon_status = bcr.validate_jirecon_section()
	if not jirecon_status:
		sys.exit("Invalid jirecon base config. exiting...")	
	