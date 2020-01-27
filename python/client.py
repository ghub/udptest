import argparse
import socket
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--hostname', default='localhost', help='the destination hostname, default to localhost')
    parser.add_argument('-p', '--port', default=8089, help='the destination port, default to 8089', type=int)
    parser.add_argument('-d', '--delay', default=0.1, help='the delay in seconds between each message, default to 0.1 seconds', type=float)
    parser.add_argument('-m', '--messages', default='./messages', help='file containing messages to send, one message per line, loops when end is reached, default to ./messages')
    parser.add_argument('-s', '--sequence', default=False, action='store_true', help='prepend sequence number, default to false')
    parser.add_argument('-t', '--timestamp', default=False, action='store_true', help='prepend timestamp , default to false')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print more info, default to false')
    return parser.parse_args()

def send_messages(args):
    if args.verbose:
        print('Send {} to {}:{} with {} seconds delay'.format(args.messages, args.hostname, args.port, args.delay))
    with open(args.messages) as f:
        lines = f.read().splitlines()
    file_line_number = 0
    message_sequence_number = 0
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            message = lines[file_line_number]
            if args.sequence:
                message = '{} {}'.format(message_sequence_number, message)
            if args.timestamp:
                timestamp = '{:.3f}'.format(time.time())
                message = '{} {}'.format(timestamp, message)
            if args.verbose:
                print(message)
            udp_socket.sendto(message, (args.hostname, args.port))
            file_line_number = (file_line_number + 1) % len(lines)
            message_sequence_number += 1
            time.sleep(args.delay)
    except KeyboardInterrupt:
        udp_socket.close()
        if args.verbose:
            print('\nSent {} messages in total'.format(message_sequence_number))
 
def main():
    args = parse_args()
    send_messages(args)
 
if __name__ == '__main__':
    main()
