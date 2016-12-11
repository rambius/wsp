#!/usr/bin/env python3.5

import http.server
import threading
import unittest
import wsp

class TestProbeServer(unittest.TestCase):

  def setUp(self):
    self.hostname = "localhost"
    self.port = 11079
    self.server = "%s:%d" % (self.hostname, self.port)
    self.thread = HTTPDThread(self.hostname, self.port)
    self.thread.start()

  def tearDown(self):
    self.thread.stop()
    if hasattr(MockHTTPRequestHandler, "wsp_response"):
      delattr(MockHTTPRequestHandler, "wsp_response")  

  def test_probe_server_header_default(self):
    spr = wsp.probe_server(self.server)
    self.assertEqual(spr.name, "BaseHTTP")
    self.assertEqual(spr.version, "0.6")
    self.assertEqual(spr.listing, wsp.DirListing.enabled)

  def test_probe_server_header_nginx_1_2_3(self):
    MockHTTPRequestHandler.server_version = "nginx/1.2.3"
    spr = wsp.probe_server(self.server)
    self.assertEqual(spr.name, "nginx")
    self.assertEqual(spr.version, "1.2.3")
    self.assertEqual(spr.listing, wsp.DirListing.enabled)

  def test_probe_server_header_iis_7_0(self):
    MockHTTPRequestHandler.server_version = "Microsoft-IIS/7.0"
    spr = wsp.probe_server(self.server)
    self.assertEqual(spr.name, "Microsoft-IIS")
    self.assertEqual(spr.version, "7.0")
    self.assertEqual(spr.listing, wsp.DirListing.enabled)

  def test_probe_server_header_nginx_1_10_2_nodl(self):
    MockHTTPRequestHandler.server_version = "nginx/1.10.2"
    MockHTTPRequestHandler.wsp_response = 403
    spr = wsp.probe_server(self.server)
    self.assertEqual(spr.name, "nginx")
    self.assertEqual(spr.version, "1.10.2")
    self.assertEqual(spr.listing, wsp.DirListing.disabled)

  def test_probe_server_header_nginx_1_11_6_unknowndl(self):
    MockHTTPRequestHandler.server_version = "nginx/1.11.6"
    MockHTTPRequestHandler.wsp_response = 401
    spr = wsp.probe_server(self.server)
    self.assertEqual(spr.name, "nginx")
    self.assertEqual(spr.version, "1.11.6")
    self.assertEqual(spr.listing, wsp.DirListing.unknown)

class MockHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

  def do_HEAD(self):
    response = 200
    if hasattr(self, "wsp_response"):
      wsp_response =  getattr(self, "wsp_response")
      response = int(wsp_response)
    self.send_response(response)
    self.end_headers()

class HTTPDThread(threading.Thread):

  def __init__(self, host="localhost", port=11079):
    server_address = (host, port)
    self.httpd = http.server.HTTPServer(server_address,
                                        MockHTTPRequestHandler)
    threading.Thread.__init__(self)

  def run(self):
    self.httpd.serve_forever()

  def stop(self):
    self.httpd.shutdown()
    self.httpd.server_close()

def main():
  unittest.main()

if __name__ == "__main__":
  main()
