from typing import Union

from dnslib import QTYPE
from dnslib.dns import DNSQuestion, RR, A

from dns.config import Config
from dns.client import DNSClient

class Hama():

	_DOMAIN = "wifiradiofrontier.com."
	_TIME_DOMAIN = "time.wifiradiofrontier.com."
	_UPDATE_DOMAIN = "update.wifiradiofrontier.com."

	def __init__(self):
		self.do_lookup = Config["DO_LOOKUP"]

	def match_domain(self, question:DNSQuestion) -> bool:
		if isinstance(question, DNSQuestion):
			if question.qname.matchSuffix(self._DOMAIN):
				if question.qtype == QTYPE.A:
					return True

		return False

	def fetch_answer(self, question:DNSQuestion) -> Union[RR, None]:
		if question.qname.matchSuffix(self._TIME_DOMAIN):
			ip_address = DNSClient.resolve_a(Config["TIME"])
		elif Config["UPDATE"] and question.qname.matchSuffix(self._UPDATE_DOMAIN):
			ip_address = DNSClient.resolve_a(self._UPDATE_DOMAIN)
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

	