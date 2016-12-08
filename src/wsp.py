#!/usr/bin/env python

import httplib
import re
import sys

class ServerProbeResult:

  def __init__(self, name=None, version=None, listing=True):
    self.name = name
    self.version = version
    self.listing = listing

def parse_server_header(server_hdr):
  m = re.match(r"([\w-]*)/([\w\.]*)", server_hdr)
  if m:
    return (m.group(1), m.group(2))
  return None 

def probe_server(server):
  conn = httplib.HTTPConnection(server)
  conn.request("HEAD", "/")
  resp = conn.getresponse()
  spr = ServerProbeResult()
  status = resp.status
  if status == httplib.FORBIDDEN:
    spr.listing = False
  server_hdr = resp.getheader('server')
  if server_hdr:
    s = parse_server_header(server_hdr)
    spr.name = s[0]
    spr.version = s[1]
  return spr

def main():
  for server in sys.argv[1:]:
    spr = probe_server(server)
    print spr.name, spr.version, spr.listing

if __name__ == '__main__':
  main()

