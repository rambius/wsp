#!/usr/bin/env python3.5

import enum
import http
import http.client
import logging
import logging.config

import re
import sys

logging.config.fileConfig("wsp-logging.conf")
logger = logging.getLogger(__name__)

class DirListing(enum.Enum):
  unknown = 0
  disabled = 1
  enabled = 2

  def __str__(self):
    return self.name

class ServerProbeResult:

  def __init__(self, name=None, version=None, listing=DirListing.enabled):
    self.name = name
    self.version = version
    self.listing = listing

def parse_server_header(server_hdr):
  m = re.match(r"([\w-]*)/([\w\.]*)", server_hdr)
  if m:
    return (m.group(1), m.group(2))
  else:
    logger.warn("Could not match header '%s'" % server_hdr)
  return None

def get_dir_listing(status):
  if status == http.HTTPStatus.FORBIDDEN:
    dl = DirListing.disabled
  elif status == http.HTTPStatus.UNAUTHORIZED:
    dl = DirListing.unknown
  else:
    dl = DirListing.enabled
  return dl

def send_request(server, method="HEAD", uri="/"):
  conn = http.client.HTTPConnection(server)
  logger.info("Sending %s request to %s" % (method, server))
  conn.request(method, uri)
  resp = conn.getresponse()
  return resp

def probe_server(server):
  resp = send_request(server) 
  spr = ServerProbeResult()
  logger.info("Status code for probing request is %d" % resp.status)
  dl = get_dir_listing(resp.status)
  spr.listing = dl
  logger.debug("Directory listing is %s" % spr.listing)
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
    print(spr.name, spr.version, spr.listing)

if __name__ == '__main__':
  main()

