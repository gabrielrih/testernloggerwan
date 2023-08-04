"""
    It tests the connection to an IP and Port through a socket.
    For testing the WAN connection for example, I recommend the use of an reliability DNS server, like Google or CloudFlare.
    Reference: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
    <gabrielrih>
"""
import socket


def test_connection_socket(host="8.8.8.8", port=53, timeout=10):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True, None
    except socket.error as ex:
        return False, str(ex)
