#!/usr/bin/env python3.5

import unittest
import wsp

class TestParseServerHeader(unittest.TestCase):

  def test_parse_nginx_1_10_2(self):
    header = "nginx/1.10.2"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "nginx", "The server does not match")
    self.assertEqual(v, "1.10.2", "The version does not match")

  def test_parse_iss_8_5(self):
    header = "Microsoft-IIS/8.5"
    (s, v) = wsp.parse_server_header(header)
    self.assertEqual(s, "Microsoft-IIS", "The server does not match")
    self.assertEqual(v, "8.5", "The version does not match")

if __name__ == "__main__":
  unittest.main()
