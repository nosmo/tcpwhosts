#!/usr/bin/env python

import unittest
import tempfile
from tcpwhosts import TCPWrapperHostsFile

FIND_ADDRESS = "74.125.24.138"
REMOVE_ADDRESS = "192.30.252.128"
NEW_ADDRESS = "10.0.0.2"
EXISTING_CONTENT = """ALL: %s
ALL: %s
""" % (REMOVE_ADDRESS, FIND_ADDRESS)

class TCPWrapperHostsFileTest(unittest.TestCase):

    def setUp(self):
        existing_filepath = tempfile.mktemp()
        with open(existing_filepath, "w") as ex_f:
            ex_f.write(EXISTING_CONTENT)
        self.tcpwfile = TCPWrapperHostsFile(existing_filepath)

    def test_file_length(self):
        self.assertEqual(len(self.tcpwfile), 2)

    def test_file_nonzero(self):
        self.assertTrue(self.tcpwfile)

    def test_file_zero(self):
        emptyfile_p = tempfile.mktemp()
        emptyfile_f = open(emptyfile_p, "w")
        emptyfile_f.close()
        emptyfile_tcpw = TCPWrapperHostsFile(emptyfile_p)
        self.assertFalse(emptyfile_tcpw)

    def test_ip_get(self):
        self.assertEqual(self.tcpwfile[FIND_ADDRESS][1], FIND_ADDRESS)

    def test_ip_exists(self):
        self.assertIn(FIND_ADDRESS, self.tcpwfile)

    def test_ip_remove(self):
        self.tcpwfile -= REMOVE_ADDRESS
        self.assertNotIn(REMOVE_ADDRESS, self.tcpwfile)

    def test_ip_add(self):
        self.tcpwfile += NEW_ADDRESS
        self.assertIn(NEW_ADDRESS, self.tcpwfile)

if __name__ == '__main__':
    unittest.main()
