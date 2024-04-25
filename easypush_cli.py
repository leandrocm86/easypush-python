import argparse
import easypush
import sys
import signal
import re
from socket import timeout

DESCRIPTION = \
    '''
====================================================================
                            Easypush

Easypush can be used in two modes: sender and listener.

- Send mode:
    To send messages, the first command must be 'send'.
    The next required argument is for recipient(s) as "HOSTS@PORT".
    There can be multiple hosts separated by comma.
    Hosts can be names or IPs (IPv4 or IPv6), including bradcast IPs.
    There can be only a single destination UDP port.
    The third positional parameter is the text to be sent.

    Examples of using Easypush for sending messages:
    easypush send 192.168.0.10@1050 'Hello World!'
    easypush send mypc.mydomain.net@1050 'Hello World!'
    easypush send 10.0.0.1,10.0.0.255@1050 'Hello Worlds!'

- Listen mode:
    For receiving messages, the first command is 'listen'.
    It must be followed by the UDP port number to listen on.
    By default, easypush waits for a message and terminates.
    The optional '-t/--timeout' parameter limits the wait in millis.

    Examples of using Easypush for listening to messages:
    easypush listen 1050  # Get first message on port 1050 and exit.
    easypush listen 1050 -t 2000  # Quit if no message comes in 2s.
    easypush listen 1050 -k  # Print all messages coming on 1050.

====================================================================
    '''

RECIPIENTS_PATTERN = r'^([a-zA-Z0-9.,:-]+)@([\d]+)$'


def out(msg: str):
    print(f'[easypush] {msg}', flush=True)


def parse_port(port: str) -> int:
    if port and port.isdigit():
        int_port = int(port)
        if 0 <= int_port <= 65535:
            return int_port
    raise argparse.ArgumentTypeError('Invalid port: it must be a number from 0 to 65535')


def parse_recipients(recipients: str) -> tuple[list[str], int]:
    if (match := re.search(RECIPIENTS_PATTERN, recipients)):
        hosts, port = match.group(1), match.group(2)
        int_port = parse_port(port)
        return hosts.split(','), int_port
    raise argparse.ArgumentTypeError('Invalid recipients format. It should be "HOSTS@PORT". Try -h for details.')


def send(args):
    hosts, port = args.RECIPIENTS
    for host in hosts:
        try:
            easypush.send([host], port, args.MESSAGE)
            out(f'Message sent to {host} on port {port}.')
        except Exception as e:
            print(f'Error when sending to host {host}: {e}', file=sys.stderr)


def listen(args):
    def handle_shutdown(signal, frame):
        out("Shutdown signaled! Terminating...")
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_shutdown)
    out(f'Starting to listen on port {args.PORT_NUMBER}')

    while True:
        try:
            msg = easypush.listen(args.PORT_NUMBER, args.timeout)
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
                sys.stderr.write(f'{e}\n')
        except Exception as e:
            sys.stderr.write(f'{e}\n')
        break


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='mode', required=True, title='mode command')

    sender_parser = subparsers.add_parser('send')
    sender_parser.add_argument('RECIPIENTS', type=parse_recipients, help='hosts and port of recipients in "HOSTS@PORT" format. Comma separated if multiple hosts.')
    sender_parser.add_argument('MESSAGE', type=str, help='text to be sent to the recipients.')

    listener_parser = subparsers.add_parser('listen')
    listener_parser.add_argument('PORT_NUMBER', type=parse_port, help='UDP port to listen on.')
    listener_parser.add_argument('-t', '--timeout', type=int, default=0, help='timeout for quitting, in milliseconds.')
    listener_parser.add_argument('-k', '--keep-alive', action='store_true', help='flag for not stopping at the first message, but to keep listening.')

    args = parser.parse_args()

    if args.mode == 'send':
        send(args)

    elif args.mode == 'listen':
        listen(args)


if __name__ == "__main__":
    main()
