# Reference: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
import socket

"""
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
"""
def test_connection_socket(host="8.8.8.8", port=53, timeout=10):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True, None
    except socket.error as ex:
        return False, str(ex)