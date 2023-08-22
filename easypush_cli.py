import argparse
import easypush
import sys
import signal
from socket import timeout

DESCRIPTION = \
    '''
====================================================================
                            Easypush

Easypush can be used in two modes: sender and listener.

- Send mode:
    To send messages, the first command must be 'send'.
    The next parameter is for recipient(s) in 'IP@PORT' format.
    There can be multiple IPs separated by comma.
    IPs can be IPv4 or IPv6 and can also be bradcast IPs.
    There can be only a single destination UDP port.
    The third and last parameter is the text to be sent.

    Examples of using Easypush for sending messages:
    easypush send 192.168.0.10@1050 'Hello World!'
    easypush send 10.0.0.1,10.0.0.255@1050 'Hello Worlds!'

- Listen mode:
    For receiving messages, the first command is 'listen'.
    It must be followed by the UDP port number to listen on.
    By default, easypush waits for a message and terminates.
    The optional '-t/--timeout' parameter limits the wait in millis.
    The optional '-k/--keep-alive' flag is to keep listening.

    Examples of using Easypush for listening to messages:
    easypush listen 1050  # Get first message on port 1050 and exit.
    easypush listen 1050 -t 2000  # Quit if no message comes in 2s.
    easypush listen 1050 -k  # Print all messages coming on 1050.

====================================================================
    '''


def out(msg: str):
    print(f'[EASYPUSH] {msg}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='mode', required=True, title='mode command')

    sender_parser = subparsers.add_parser('send')
    sender_parser.add_argument('RECIPIENTS', type=str, help='IP(s) and port of recipients in "IPs@PORT" format. Comma separated if multiple IPs.')
    sender_parser.add_argument('MESSAGE', type=str, help='Text to be sent to the recipients.')

    listener_parser = subparsers.add_parser('listen')
    listener_parser.add_argument('PORT_NUMBER', type=int, help='UDP port to listen on.')
    listener_parser.add_argument('-t', '--timeout', type=int, default=0, help='Timeout for quitting, in milliseconds.')
    listener_parser.add_argument('-k', '--keep-alive', action='store_true', help='Flag for not stopping at the first message, but to keep listening.')

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
            out("Shutdown signaled! Terminating...")
            sys.exit(0)

        signal.signal(signal.SIGTERM, handle_shutdown)

        out(f'Starting to listen on port {args.PORT_NUMBER}')

        while True:
            try:
                msg = easypush.listen(parse_port(args.PORT_NUMBER), args.timeout)
                out('Received message: ' + msg)
                if args.keep_alive:
                    continue
            except KeyboardInterrupt:
                out("Interrupted by user.")
            except timeout:
                out('Timeout reached for listener.')
            except OSError as e:
                if e.errno == 98:
                    out('Port seems to be already in use!')
                else:
                    raise e
            break


if __name__ == "__main__":
    main()
