
import os, re
import ipaddress

class Config():

	# Regex from https://github.com/kvesteri/validators/
	# 	MIT License, Copyright (c) 2013-2014 Konsta Vesterinen
	_domain_pattern = re.compile(
		r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
		r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
		r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
		r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
	)

	_data = {}
	_init_done = False

	def _load_data(cls):
		cls._data = {
			"BIND": str(os.getenv("SERVER_BIND", "0.0.0.0")),
			"PORT": int(os.getenv("SERVER_PORT", 53)),
			"UPSTREAM": str(os.getenv("SERVER_UPSTREAM", "8.8.8.8")),
			"RADIO": str(os.getenv("RADIO_DOMAIN", os.getenv("RADIO_IP", None))),
			"TIME" : str(os.getenv("TIME_SERVER", "ntp0.fau.de")),
			"ALLOWED" : str(os.getenv("ALLOWED_DOMAIN", "all")),
			"DEVMODE" : bool(os.getenv("DEVMODE", "false") == "true")
		}

		radio_is_ip, radio_is_domain = True, True

		if cls._data["RADIO"] is None:
			raise RuntimeError("$ENV[RADIO_DOMAIN] and $ENV[RADIO_IP] not set")

		for (k,n) in [("BIND", "SERVER_BIND"), ("UPSTREAM", "SERVER_UPSTREAM"), ("RADIO", "RADIO_IP")]:
			try:
				ipaddress.ip_address(cls._data[k])	
			except ValueError:
				if k == "RADIO":
					radio_is_ip = False # value "RADIO" is not an ip address!
				else:
					raise RuntimeError("$ENV[%s] invalid IP address" % n)

		for (k,n) in [("RADIO", "RADIO_DOMAIN"), ("TIME", "TIME_SERVER")]:
			if not cls._validate_domain(cls, cls._data[k]):
				if k == "RADIO":
					radio_is_domain = False # value "RADIO" is not a domain!
				else:
					raise RuntimeError("$ENV[%s] invalid domain name" % n)

		if not radio_is_domain and not radio_is_ip:
			raise RuntimeError("$ENV[RADIO_DOMAIN] is no domain and $ENV[RADIO_IP] is no IP address!")
		cls._data["DO_LOOKUP"] = radio_is_domain

		if cls._data["ALLOWED"] != "all":
			cls._data["ALLOWED"] = cls._data["ALLOWED"].split(",")
			cls._data["ALLOWED_ALL"] = False 

			for allowed in cls._data["ALLOWED"]:
				if not cls._validate_domain(cls, allowed):
					raise RuntimeError("$ENV[ALLOWED] contains invalid domain name '%s'" % allowed)
		else:
			del cls._data["ALLOWED"]
			cls._data["ALLOWED_ALL"] = True 

		cls._init_done = True

	def _validate_domain(cls, domain : str):
		return not cls._domain_pattern.match(domain) is None

	def __class_getitem__(cls, key:str):
		if not cls._init_done:
			cls._load_data(cls)

		if key in cls._data:
			return cls._data[key]
		elif key.upper() in cls._data:
			return cls._data[key.upper()]
		
		raise KeyError("No config entry for key '%s'!" % key)
