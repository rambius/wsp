#!/usr/bin/env python

import httplib
import logging
import re
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ServerProbeResult:

  def __init__(self, name=None, version=None, listing=True):
    self.name = name
    self.version = version
    self.listing = listing

def parse_server_header(server_hdr):
  m = re.match(r"([\w-]*)/([\w\.]*)", server_hdr)
  if m:
    logger.info("Found match in header '%s'" % server_hdr)
    return (m.group(1), m.group(2))
  return None 

def probe_server(server):
  conn = httplib.HTTPConnection(server)
  method = "HEAD"
  logger.info("Sending %s request to %s" % (method, server))
  conn.request(method, "/")
  resp = conn.getresponse()
  spr = ServerProbeResult()
  logger.info("Status code for %s request is %d" % (method, resp.status))
  if resp.status == httplib.FORBIDDEN:
    spr.listing = False
  server_hdr = resp.getheader('server')
  logger.debug("Found server header '%s'" % server_hdr)
  if server_hdr:
    s = parse_server_header(server_hdr)
    spr.name = s[0]
    spr.version = s[1]
  return spr

def main():
  for server in sys.argv[1:]:
    logger.debug("Probing %s" % server)
    spr = probe_server(server)
    print spr.name, spr.version, spr.listing

if __name__ == '__main__':
  main()

