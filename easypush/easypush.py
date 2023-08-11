import socket


def send(hosts: list[str], port: int, message: str):
    """
    Sends an UDP message to one or more hosts.

    Args:
        hosts (list[str]): A list of host addresses to send the message to. They can be in either IPv4 or IPv6 format.
        port (int): The port number to send the message to.
        message (str): The message to be sent.
    """
    for host in hosts:
        family = socket.AF_INET if '.' in host else socket.AF_INET6
        with socket.socket(family, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enables broadcast
            msg_bytes = bytes(message, 'utf-8')
            sock.sendto(msg_bytes, (host, port))


def listen(port: int, timeout: int = 0) -> str:
    """
    Listens for incoming UDP packets on the specified port.

    Args:
        port (int): The port number to listen on.
        timeout (int, optional): The timeout value in milliseconds. Defaults to 0 (no timeout).

    Returns:
        str: The received message as a string.
    """
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)  # Enables both IPv6 and IPv4
        if timeout:
            sock.settimeout(timeout / 1000)
        sock.bind(("::", port))
        data, addr = sock.recvfrom(1024)
        return data.decode('utf-8')
