#!/usr/bin/env python3.5

import argparse
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
  regexps = [r"([\w-]*)/([\w\.]*)", r"(nginx|Microsoft-IIS)"]
  for regexp in regexps:
    m = re.match(regexp, server_hdr)
    if m:
      if len(m.groups()) == 2: 
        return (m.group(1), m.group(2))
      elif len(m.groups()) == 1:
        return (m.group(1), None)

  logger.warning("Could not match header '%s' against regexps" % server_hdr)
  return (None, None)

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

def compare_server_version(spr, versions):
  return (spr.name in versions) and spr.version and spr.version.startswith(versions[spr.name])

def probe_servers(servers, versions):
  for server in servers:
    logger.debug("Probing %s" % server)
    spr = probe_server(server)
    if (compare_server_version(spr, versions)):
        print("MATCH:", spr.name, spr.version, spr.listing)
    else:
      print("NO MATCH:", spr.name, spr.version, spr.listing) 

def main():
  description = "Probes a web server" 
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("-n", "--nginx", 
                      default="1.2",
                      help="nginx's verion to look for")
  parser.add_argument("-i", "--iis",
                      default="7.0",
                      help="iis's version to look for")
  parser.add_argument("server",
                      nargs='+',
                      help="a server that will be probed")
  args = parser.parse_args()
  versions = {"nginx": args.nginx, "Microsoft-IIS": args.iis}
  
  probe_servers(args.server, versions)

if __name__ == '__main__':
  main()

