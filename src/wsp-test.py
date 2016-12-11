#!/usr/bin/env python3.5

import http
import unittest
import wsp

class TestParseServerHeader(unittest.TestCase):

  def test_parse_nginx_1_10_2(self):
    header = "nginx/1.10.2"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "nginx", "server parsed incorrectly")
    self.assertEqual(v, "1.10.2", "version parsed incorrectly")

  def test_parse_iss_8_5(self):
    header = "Microsoft-IIS/8.5"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "Microsoft-IIS", "server parsed incorrectly")
    self.assertEqual(v, "8.5", "version parsed incorrectly")

  def test_parse_nginx_noversion(self):
    header = "nginx"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "nginx", "server parsed incorrectly")
    self.assertIsNone(v, "version parsed incorrectly")

  def test_parse_iis_noversion(self):
    header = "Microsoft-IIS"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "Microsoft-IIS", "server parsed incorrectly")
    self.assertIsNone(v, "version parsed incorrectly")

  def test_parse_unknown(self):
    header = "unknown"
    (s, v) = wsp.parse_server_header(header)
    self.assertIsNone(s, "server parsed incorrectly")
    self.assertIsNone(v, "version parsed incorrectly")

class TestGetDirListing(unittest.TestCase):
  
  def test_get_dir_listing_ok(self):
    dl = wsp.get_dir_listing(http.HTTPStatus.OK)
    self.assertEqual(dl, wsp.DirListing.enabled)

  def test_get_dir_listing_uknown(self):
    dl = wsp.get_dir_listing(http.HTTPStatus.UNAUTHORIZED)
    self.assertEqual(dl, wsp.DirListing.unknown)

  def test_get_dir_listing_disabled(self):
    dl = wsp.get_dir_listing(http.HTTPStatus.FORBIDDEN)
    self.assertEqual(dl, wsp.DirListing.disabled)

class TestCompareServerVersion(unittest.TestCase):

  def setUp(self):
    self.versions = {"nginx": "1.2", "Microsoft-IIS": "7.0"}

  def test_compare_nginx_version_no(self):
    spr = wsp.ServerProbeResult("nginx", "1.16.1")
    self.assertFalse(wsp.compare_server_version(spr, self.versions))

  def test_compare_nginx_version_yes(self):
    spr = wsp.ServerProbeResult("nginx", "1.2.3")
    self.assertTrue(wsp.compare_server_version(spr, self.versions))

  def test_compare_iss_version_no(self):
    spr = wsp.ServerProbeResult("Microsoft-IIS", "8.5")
    self.assertFalse(wsp.compare_server_version(spr, self.versions))
   
  def test_compare_iis_version_yes(self):
    spr = wsp.ServerProbeResult("Microsoft-IIS", "7.0")
    self.assertTrue(wsp.compare_server_version(spr, self.versions))

  def test_compare_nginx_none_version(self):
    spr = wsp.ServerProbeResult("nginx")
    self.assertFalse(wsp.compare_server_version(spr, self.versions))

  def test_compare_iis_none_version(self):
    spr = wsp.ServerProbeResult("Microsoft-IIS")
    self.assertFalse(wsp.compare_server_version(spr, self.versions))

if __name__ == "__main__":
  unittest.main()
