# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from msgBrowserLayout import *
from ContactListLayout import *
from ClientServerListener import Listener
import sys
import socket
import json


host = 'localhost'
port = 56188
server_addr = (host, port)

#Constants
DEFAULT_MSG = 'hello!'
ACCEPT_MSG = '0001'
MESSAGE = '2222'
ACCEPT_CONTACT_LIST = '0003'
ADD_CONTACT = '0103'
DEL_CONTACT = '0013'


class ChatLogin(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi('login.ui', self)
        self.loginBtn.clicked.connect(self.login)
        self.show()
        self.move(400,300)

    def login(self):
        name = self.userName.toPlainText().toUtf8()
        if name != '':
            self.chat = ChatApp(name=name)
            self.chat.show()
            self.close()


class ChatApp(QtGui.QWidget):
    def __init__(self,name='anonymuser', parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('chat.ui', self)
        self.move(200,200)
        self.current_dialog = ''
        self.user_name = str(name)
        self.db = {}
        data = self.send_msg_to_server(action='1111', _from=self.user_name)
        print data
        data = json.loads(data)
        self.ip_addr = data['ip']
        self.listener = Listener(self.ip_addr)
        self.listener.start()
        self.msgSend.clicked.connect(self.send_msg)
        self.connect(self.listener, QtCore.SIGNAL('MsgSignal(QString)'), self.recv, QtCore.Qt.QueuedConnection)
        self.send_msg_to_server(action='4444', _from=self.ip_addr)
        self.contactList.itemClicked.connect(self.itemClickContact)


    def send_msg_to_server(self, action='', msg='', _from='', to=''):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr)
        data = json.dumps({'action': action,
                           'from': _from,
                           'to': to,
                           'message': msg })
        sock.send(data)
        data = sock.recv(1024)
        sock.close()
        return data

    def itemClickContact(self, item):
        if self.current_dialog != item.ip:
            self.current_dialog = item.ip
            self.msgBrowser.clear()
            for item in self.db[item.ip]:
                self.add_text_msg(item[0], item[1])

    def initial_contact_list(self, data):
        for key in data:
            if key != self.ip_addr:
                self.db[key] = []
                self.add_contcact(data[key]['name'], key)

    def update_contact_list(self, action, data):
        if action == ADD_CONTACT:
            self.db[data['ip']] = []
            self.add_contcact(data['name'], data['ip'])
        elif action == DEL_CONTACT:
            self.db.pop(data['ip'])
            if self.current_dialog == data['ip']:
                self.current_dialog = ''
                self.msgBrowser.clear()
            for i in xrange(self.contactList.count()):
                if self.contactList.item(i).ip == data['ip']:
                    self.contactList.takeItem(self.contactList.row(self.contactList.item(i)))
                    break

    def add_contcact(self, name, ip):
        # tem_base = QtGui.QListWidgetItem()
        item_base = IItem(ip)
        item = ContactItem(name, ip)
        item_base.setSizeHint(item.sizeHint())
        self.contactList.addItem(item_base)
        self.contactList.setItemWidget(item_base, item)


    def recv(self, s):
        data = json.loads(str(s))
        if data['action'] == ACCEPT_MSG:
            self.db[data['from']].append([data["message"], False])
            if data['from'] == self.current_dialog:
                self.add_text_msg(data['message'])
        elif data['action'] == ACCEPT_CONTACT_LIST:
            self.initial_contact_list(data['message'])
        elif data['action'] == ADD_CONTACT or data['action'] == DEL_CONTACT:
            self.update_contact_list(data['action'], data['message'])


    def closeEvent(self, event):
        self.listener.run_flag = False
        self.send_msg_to_server(action='3333', _from=self.ip_addr)
        event.accept()


    def add_text_msg(self,text=DEFAULT_MSG, lr=False):
        item_base = QtGui.QListWidgetItem(self.msgBrowser)
        wid = self.msgBrowser.size().width()
        item = TextItem(item_base, self.msgBrowser, text, lr)
        item.setEnabled(False)
        item_base.setSizeHint(item.sizeHint())
        item_base.setFlags(QtCore.Qt.ItemIsEnabled)
        self.msgBrowser.addItem(item_base)
        self.msgBrowser.setItemWidget(item_base, item)
        self.msgBrowser.setCurrentItem(item_base)

    def send_msg(self):
        msg_txt = str(self.msgInput.toPlainText().toUtf8())
        msg_txt = msg_txt.decode('utf-8')
        self.msgInput.clear()
        self.add_text_msg(msg_txt, True)
        if self.current_dialog != '':
            self.db[self.current_dialog].append([msg_txt, True])
        self.send_msg_to_server(action=MESSAGE, to=self.current_dialog, _from=self.ip_addr, msg=msg_txt)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    chat_window = ChatLogin()
    sys.exit(app.exec_())
