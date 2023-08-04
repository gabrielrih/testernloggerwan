from unittest import TestCase

from src.libs.connection import test_connection_socket


class TestConnection(TestCase):
    def test_connection_socket_when_success(self):
        success, message = test_connection_socket()
        self.assertTrue(success)
        self.assertEqual(message, None)

    def test_connection_socket_when_it_fails(self):
        success, message = test_connection_socket(host='1.2.3.4', port=54, timeout=5)
        self.assertFalse(success)
        self.assertEqual(message, 'timed out')