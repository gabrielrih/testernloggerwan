# Reference: https://docs.python.org/3/library/urllib.request.html
import urllib.request
from urllib.error import URLError, HTTPError
import socket

"""
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    Reference: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
"""
def test_connection_socket(host="8.8.8.8", port=53, timeout=10):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True, None
    except socket.error as ex:
        return False, str(ex)


def test_connection_url(url='https://www.google.com', timeout=10):
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
    except timeout:
        return False, "Request has reached the timeout!"
    except HTTPError as e:
        return False, str(e.reason)
    except URLError as e:
        return False, str(e.reason)
    else:
        return True, None