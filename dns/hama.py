from typing import Union

from dnslib import QTYPE
from dnslib.dns import DNSQuestion, RR, A

from dns.config import Config
from dns.client import DNSClient

class Hama():

	_DOMAINS = ("wifiradiofrontier.com.", "internetradiofrontier.com.")
	_TIME_SUB_DOMAIN = "time.*"
	_UPDATE_SUB_DOMAIN = "update.*"

	def __init__(self):
		self.do_lookup = Config["DO_LOOKUP"]

	def match_domain(self, question:DNSQuestion) -> bool:
		if isinstance(question, DNSQuestion):
			if any(question.qname.matchSuffix(domain) for domain in self._DOMAINS):
				if question.qtype == QTYPE.A:
					return True

		return False

	def fetch_answer(self, question:DNSQuestion) -> Union[RR, None]:
		if question.qname.matchGlob(self._TIME_SUB_DOMAIN):
			ip_address = DNSClient.resolve_a(Config["TIME"])
		elif Config["UPDATE"] and question.qname.matchGlob(self._UPDATE_SUB_DOMAIN):
			ip_address = DNSClient.resolve_a(str(question.qname))
		else:
			ip_address = DNSClient.resolve_a(Config["RADIO"]) if self.do_lookup else Config["RADIO"]

		if ip_address == None:
			return None
		else:
			return RR(
				question.qname,
				QTYPE.A,
				rdata=A(ip_address),
				ttl=300
			)

	