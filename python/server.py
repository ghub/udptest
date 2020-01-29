import argparse
import socket
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8089, help='the bind port, default to 8089', type=int)
    parser.add_argument('-s', '--sequence', default=False, action='store_true', help='prepend sequence number, default to false')
    parser.add_argument('-t', '--timestamp', default=False, action='store_true', help='prepend timestamp, default to false')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print more info, default to false')
    return parser.parse_args()

def receive_messages(args):
    if args.verbose:
        print('Listening on port {}'.format(args.port))
    message_sequence_number = 0
    try:
        host = '0.0.0.0'
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((host, args.port))
        if args.verbose:
            print('RCVBUF={}'.format(udp_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
        buffer_size = 1024 * 1024
        while True:
            message, _address = udp_socket.recvfrom(buffer_size)
            if not message:
                continue
            message = message.decode()
            if args.sequence:
                message = '{} {}'.format(message_sequence_number, message)
            if args.timestamp:
                timestamp = '{:.3f}'.format(time.time())
                message = '{} {}'.format(timestamp, message)
            if args.verbose:
                print(message)
            message_sequence_number += 1
    except KeyboardInterrupt:
        udp_socket.close()
        if args.verbose:
            print('\nReceived {} messages in total'.format(message_sequence_number))

def main():
    args = parse_args()
    receive_messages(args)

if __name__ == '__main__':
    main()
