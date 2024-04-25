# Radio DNS Server
for https://github.com/KIMB-technologies/Radio-API

> See the Docker Image at https://hub.docker.com/r/kimbtechnologies/radio_dns  
> Github Action build of https://github.com/KIMB-technologies/Radio-DNS-Server

## Configuration

The configuration is done using env variables.

- `SERVER_BIND` *(optional, default `0.0.0.0`)* The IP address the server binds on. `0.0.0.0` binds on all interfaces.
- `SERVER_PORT` *(optional, default `53`)* The port which is used for the DNS server, should always be the default `53` (unless for testing).
- `SERVER_UPSTREAM` *(optional, default `8.8.8.8`)* The upstream DNS server, where DNS answers are fetched from 
- `RADIO_DOMAIN` *(required, if `RADIO_IP` not set)* The domain where the [Radio-API](https://github.com/KIMB-technologies/Radio-API) can be found.
	The DNS server will return the `A` record of this domain for all queries containing `wifiradiofrontier.com`. 
- `RADIO_IP` *(required, if `RADIO_DOMAIN` not set)* The ip address where the [Radio-API](https://github.com/KIMB-technologies/Radio-API) can be found.
	The DNS server will return this IP for all queries containing `wifiradiofrontier.com`. 
	If `RADIO_DOMAIN` is set, it will be used. If `RADIO_DOMAIN` is not set, `RADIO_IP` will be used!
- `ALLOWED_DOMAIN` *(optional, default `all`)* Normally a DNS resolver will answer all queries from all sources. This can be a security risk, so one should only answer the queries from trusted sources. One can give a list (domain names divided by `,`) of domain name here, only queries from the corresponding `A` records will be answered then.  **The default value is `all` which means all sources are trusted. E.g. for testing and usage in local networks.** (Normally giving your DynDNS name is right; More domain names lead to a higher response time to queries.)
- `TIME_SERVER` *(optional, default `ntp0.fau.de`)* If the DNS server is queried for `time.wifiradiofrontier.com` it will answer with the `A` record of this domain. So one does not have to host an own NTP server at `RADIO_DOMAIN`. Per default some time server is used.
- `ENABLE_UPDATE` *(optional, default `false`)* Set to `true` to enable responding to DNS queries for `update.wifiradiofrontier.com` with the `A` record of `update.wifiradiofrontier.com` instead of the ip of Radio-API. (This will allow the radio to do updates. Performing updates is a trade-off between risking changes to the API, that may prevent Radio-API from working, and bug fixes and security implications for the radio's software.)

Run using the [**Docker-compose Example**](./docker-compose.yml)!

## Notice and Used Libraries
- Alpine [Docker Image](https://hub.docker.com/_/alpine)
- [Python 3](https://www.python.org/)
- Python [DnsLib](https://pypi.org/project/dnslib/)
- Code inspired from [DNSServer](https://github.com/samuelcolvin/dnserver)  
  MIT License, Copyright (c) 2017 Samuel Colvin
- Regex Pattern from [Validators](https://github.com/kvesteri/validators/) used  
  MIT License, Copyright (c) 2013-2014 Konsta Vesterinen