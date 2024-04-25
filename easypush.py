import socket


def send(hosts: list[str], port: int, message: str):
    """
    Sends an UDP message to one or more hosts.

    Args:
        hosts (list[str]): A list of host addresses to send the message to. They can be names or IPs (IPv4 or IPv6).
        port (int): The port number to send the message to.
        message (str): The message to be sent.
    """
    for host in hosts:

        # Checks if host is a domain name (has letters but it's not IPv6) and resolve it to an IP.
        if ':' not in host and any(char.isalpha() for char in host):
            try:
                ip_addresses = [info[4][0] for info in socket.getaddrinfo(host, None)]
                assert ip_addresses
            except Exception:
                raise ValueError(f'Could not resolve name: {host}')

            if len(set(ip_addresses)) > 1:
                print(f'Name {host} resolves to different IPs: {set(ip_addresses)}. Picking {ip_addresses[0]}...')

            if ':' in ip_addresses[0]:
                print(f'Host {host} resolved to an IPv6 address:', ip_addresses[0])

            host = ip_addresses[0]

        # Dinamically determine the protocol family (ipv4 or ipv6) based on the host address.
        family = socket.AF_INET6 if ':' in host else socket.AF_INET

        protocol = socket.SOCK_DGRAM  # socket.SOCK_STREAM for TCP
        with socket.socket(family, protocol) as sock:
            _send_udp(host, port, message, sock)


def _send_udp(host: str, port: int, message: str, sock: socket.socket):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enables broadcast
    msg_bytes = bytes(message, 'utf-8')
    sock.sendto(msg_bytes, (host, port))


# def _send_tcp(host: str, port: int, message: str, sock: socket.socket):
#     sock.connect((host, port))
#     msg_bytes = bytes(message, 'utf-8')
#     sock.sendall(msg_bytes)
    # Receive a response from the server (optional)
    # response = sock.recv(1024)  # Adjust buffer size as needed
    # print("Received response:", response.decode('utf-8'))


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
        return _listen_udp(port, timeout, sock)


def _listen_udp(port: int, timeout: int, sock: socket.socket) -> str:
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)  # Enables both IPv6 and IPv4
    if timeout:
        sock.settimeout(timeout / 1000)
    sock.bind(("::", port))
    data, addr = sock.recvfrom(1024)
    return data.decode('utf-8')


# def _listen_tcp(port: int, timeout: int, sock: socket.socket) -> str:
#     sock.bind(("localhost", port))  # Bind to localhost (modify if needed)
#     sock.listen(1)  # Listen for incoming connections (queue length of 1)
#     if timeout:
#         sock.settimeout(timeout)  # Set timeout in seconds
#     conn, addr = sock.accept()  # Wait for a connection
#     with conn:  # Use context manager to ensure proper closing
#         data = conn.recv(1024).decode('utf-8')
#         return data
