# -*- coding: utf-8 -*-
import SocketServer
import json
import socket
from multiprocessing import Process

LOGIN = '1111'
MESSAGE = '2222'
LOGOUT = '3333'
GET_CONTACTS = '4444'

host = 'localhost'
port = 56188
addr = (host, port)

data_base = {}
used_ip = [['127.0.0.{}'.format(i), False] for i in xrange(2,250)]


def inform_users(action, name, ip):
    for item in used_ip:
        if item[1]:
            if item[0] != ip:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((item[0], port))
                info = json.dumps({
                    'action': action,
                    'from': 'server',
                    'to': item[0],
                    'message':{
                        'name':name,
                        'ip': ip
                    }
                })
                sock.send(info)
                sock.close()




def get_free_addr():
    for ip_addr in used_ip:
        if ip_addr[1] == False:
            used_ip[used_ip.index(ip_addr)][1] = True
            return ip_addr
    return None

def loose_ip(ip):
    used_ip[used_ip.index([ip, True])][1] = False


class TCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        data = json.loads(self.data)
        print data
        if data['action'] == LOGIN:
            ip = get_free_addr()[0]
            respons = {'ip': ip}
            respons = json.dumps(respons)
            data_base[ip] = {
                'name': data['from']
            }
            print "connected: {} {}".format(data['from'], ip)
            self.request.sendall(respons)
            p = Process(target=inform_users, args=('0103', data['from'], ip))
            p.start()
            p.join()
            #inform_users('0103', data['from'] ,ip)

        elif data['action'] == LOGOUT:
            name = data_base[data['from']]['name']
            data_base.pop(data['from'])
            loose_ip(data['from'])
            print "disconnected: {}".format(data['from'])
            p = Process(target=inform_users, args=('0013', name, data['from']))
            p.start()
            p.join()
            #inform_users('0013', name , data['from'])

        elif data['action'] == MESSAGE:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                user = data_base[data['to']]
                sock.connect((data['to'], port))
                data = json.dumps({'action': '0001',
                                   'from': data['from'],
                                   'to': data["to"],
                                   'message': data['message']})
                sock.send(data)
                print "send 1"
            except :
                sock.connect((data['from'], port))
                data = json.dumps({'action': '0001',
                                   'from': 'server',
                                   'to': data["from"],
                                   'message': 'user is  offline'})
                sock.send(data)
                print 'send 2'
            sock.close()
            print 'close sock'
        elif data['action'] == GET_CONTACTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((data['from'], port))
            data = json.dumps({'action': '0003',
                               'from': "server",
                               'to': data["from"],
                               'message': data_base})
            sock.send(data)
            sock.close()
        else:
            self.request.sendall()


if __name__ == '__main__':
    server = SocketServer.TCPServer(addr, TCPHandler)
    print 'starting server.... for exit press Ctrl+c'
    server.serve_forever()
