from unittest import TestCase

from src.libs.connection import test_connection_socket


class TestConnection(TestCase):
    def test_connection_socket_when_success(self):
        success, message = test_connection_socket()
        self.assertTrue(success)
        self.assertIsNone(message)

    def test_connection_socket_when_timed_out(self):
        success, message = test_connection_socket(host='1.2.3.4', port=54, timeout=1)
        self.assertFalse(success)
        self.assertEqual(message, 'timed out')
