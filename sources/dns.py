import dns.resolver

class DNSSource:
    def __init__(self):
        self.name = "dns"

    def analyze_domain(self, domain: str) -> dict:
        result = {}
        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS']
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                result[rtype] = [str(rdata) for rdata in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
                result[rtype] = []
            except Exception as e:
                 result[rtype] = [f"Error: {str(e)}"]
                 
        return result
