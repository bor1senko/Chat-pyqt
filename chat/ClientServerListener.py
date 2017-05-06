# -*- coding: utf-8 -*-
import SocketServer
import json
import socket

from PyQt4 import QtCore, QtGui, uic


class Listener(QtCore.QThread):
    def __init__(self,ip='', parent=None):
        self.addr =(ip, 56188)
        print self.addr
        self.run_flag = True
        QtCore.QThread.__init__(self, parent)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.addr)
        s.listen(250)
        print 'run socket'
        while self.run_flag:
            conn, addr = s.accept()
            print conn, addr
            data = conn.recv(1024)
            print data
            self.emit(QtCore.SIGNAL('MsgSignal(QString)'),'%s' % data)
            conn.send(json.dumps({'action':'ok'}))
        print 'close socket'
        conn.close()
        s.close()
