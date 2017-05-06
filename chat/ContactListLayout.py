from PyQt4 import QtCore, QtGui, uic




class ContactItem(QtGui.QWidget):
    def __init__(self, name, ip):
        super(ContactItem, self).__init__()
        self.ip = ip
        hbox = QtGui.QHBoxLayout()
        name = QtGui.QLabel(name)
        name.setStyleSheet("QLabel {background-color:transparent; color: #383838;}")
        count_msg = QtGui.QLabel('+1')
        count_msg.setStyleSheet("QLabel { background-color:transparent; color: #383838;}")
        hbox.addWidget(name)
        hbox.addStretch()
        hbox.addWidget(count_msg)
        self.setLayout(hbox)


class IItem(QtGui.QListWidgetItem):
    def __init__(self, ip):
        super(IItem, self).__init__()
        self.ip = ip
