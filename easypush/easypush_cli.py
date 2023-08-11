import argparse
from . import easypush
import sys
import signal
from socket import timeout

DESCRIPTION = \
    '''
====================================================================
                            EasyPush

EasyPush can be used in two modes: sender and listener.

- Send mode:
    To send messages, the first parameter must be 'send'.
    The second parameter is for recipient(s) in 'IP@PORT' format.
    There can be multiple IPs separated by comma.
    IPs can be IPv4 or IPv6 and can also be bradcast IPs.
    There can be only a single destination UDP port.
    The third and last parameter is the text to be sent.

    Examples of using EasyPush for sending messages:
    easypush send 192.168.0.10@1050 'Hello World!'
    easypush send 10.0.0.1,10.0.0.255@1050 'Hello Worlds!'

- Listen mode:
    For receiving messages, the first parameter is 'listen'.
    The second parameter is the UDP port to listen on.
    There's an optional '-t' or '--timeout' parameter.
    Easypush quits if no message arrives before a timeout.
    If given no timeout, EasyPush keeps listening until terminated.

    Examples of using EasyPush for listening to messages:
    easypush listen 1050  # Prints all messages coming on port 1050.
    easypush listen 1050 -t 1000  # Waits for a message for 1s max.

====================================================================
    '''


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='mode', required=True)

    sender_parser = subparsers.add_parser('send')
    sender_parser.add_argument('RECIPIENTS', type=str, help='IP(s) and port of recipients in "IPs@PORT" format. Comma separated if multiple IPs.')
    sender_parser.add_argument('MESSAGE', type=str, help='Text to be sent to the recipients.')

    listener_parser = subparsers.add_parser('listen')
    listener_parser.add_argument('PORT', type=int, help='UDP port to listen on.')
    listener_parser.add_argument('-t', '--timeout', type=int, default=0, help='Timeout in milliseconds for quitting if no message arrives.')

    args = parser.parse_args()

    def parse_port(port: int | str | None) -> int:
        int_port = port if isinstance(port, int) else None
        if isinstance(port, str) and port.isdigit():
            int_port = int(port)
        elif not int_port or not (0 <= int_port <= 65535):
            sys.stderr.write('Invalid port: it must be a number from 0 to 65535\n')
            sys.exit(1)
        assert isinstance(int_port, int) and 0 <= int_port <= 65535
        return int_port

    if args.mode == 'send':
        ips, _, port = args.RECIPIENTS.partition('@')
        recipients = ips.split(',')
        int_port = parse_port(port)
        easypush.send(recipients, int_port, args.MESSAGE)
    elif args.mode == 'listen':

        def handle_shutdown(signal, frame):
            print("[EASYPUSH] System shutting down.")
            sys.exit(0)

        signal.signal(signal.SIGTERM, handle_shutdown)

        def listen():
            try:
                msg = easypush.listen(parse_port(args.PORT), args.timeout)
                print('[EASYPUSH] Received message:', msg)
            except KeyboardInterrupt:
                print("[EASYPUSH] Interrupted by user.")
                sys.exit(0)

        if args.timeout:
            try:
                print('[EASYPUSH] Waiting for message on port', args.PORT)
                listen()
            except timeout:
                print('[EASYPUSH] Timeout reached for listener.')
        else:
            print('[EASYPUSH] Starting to listen on port', args.PORT)
            while True:
                listen()


if __name__ == "__main__":
    main()
