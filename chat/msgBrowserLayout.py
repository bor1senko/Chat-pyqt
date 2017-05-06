from PyQt4 import QtCore, QtGui, uic
from math import *

DEFAULT_MSG = 'hello'



class BubbleTextMsg(QtGui.QLabel):
    border = 5
    trigon = 20
    lineLen = 40

    minH = 2 * trigon + 2 * border
    minW = 2 * trigon + 2 * border

    def __init__(self,listItem,listView,text = DEFAULT_MSG,lr = True):
        self.listItem = listItem
        self.listView = listView
        self.text = text
        # myText = splitStringByLen(text, self.lineLen)
        myText = text

        super(BubbleTextMsg, self).__init__(myText)

        self.setMinimumWidth(self.minW)
        # !self.setFont(QFont("Times",20,QFont.Normal))
        self.setStyleSheet("QLabel {background-color:transparent; color: #383838;}")
        self.setState(False)

        self.lr = lr
        if self.lr:

            self.setContentsMargins(self.trigon*sqrt(3)/2 + 3,self.border + 3,self.border + 3,self.border + 3)
        else:
            self.setContentsMargins(self.border + 3,self.border + 3,self.trigon*sqrt(3)/2 + 3,self.border + 3)

    def paintEvent(self, e):
        size =  self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.lr:
            self.leftBubble(qp,size.width(),size.height())
        else:
            self.rightBubble(qp,size.width(),size.height())
        qp.end()
        super(BubbleTextMsg, self).paintEvent(e)

    def leftBubble(self,qp, w, h):
        qp.setPen(self.colorLeftE)
        qp.setBrush(self.colorLeftM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QtGui.QPolygonF()
        pL.append(QtCore.QPointF(0,middle))
        pL.append(QtCore.QPointF(shiftx, middle + shifty))
        pL.append(QtCore.QPointF(shiftx, h - self.border))
        pL.append(QtCore.QPointF(w - self.border, h - self.border))
        pL.append(QtCore.QPointF(w - self.border, self.border))
        pL.append(QtCore.QPointF(shiftx, self.border))
        pL.append(QtCore.QPointF(shiftx, middle - shifty))
        qp.drawPolygon(pL)

    def rightBubble(self, qp, w, h):
        qp.setPen(self.colorRightE)
        qp.setBrush(self.colorRightM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QtGui.QPolygonF()
        pL.append(QtCore.QPointF(w,middle))
        pL.append(QtCore.QPointF(w - shiftx, middle + shifty))
        pL.append(QtCore.QPointF(w - shiftx, h - self.border))
        pL.append(QtCore.QPointF(self.border, h - self.border))
        pL.append(QtCore.QPointF(self.border, self.border))
        pL.append(QtCore.QPointF(w - shiftx, self.border))
        pL.append(QtCore.QPointF(w - shiftx, middle - shifty))
        qp.drawPolygon(pL)

    def setState(self,mouse):
        if mouse:
            self.colorLeftM = QtGui.QColor("#eaeaea")
            self.colorLeftE = QtGui.QColor("#D6D6D6")
            self.colorRightM = QtGui.QColor("#8FD648")
            self.colorRightE = QtGui.QColor("#85AF65")
        else:
            self.colorLeftM = QtGui.QColor("#fafafa")
            self.colorLeftE = QtGui.QColor("#D6D6D6")
            self.colorRightM = QtGui.QColor("#9FE658")
            self.colorRightE = QtGui.QColor("#85AF65")
        self.update()

    def enterEvent(self,e):
        # print 'mouse entered'
        self.setState(True)
    def leaveEvent(self,e):
        # print 'mouse leaved'
        self.setState(False)

    def contextMenuEvent(self,e):
        editUser = QAction(QIcon('icons/copy.png'),u'copy',self)
        editUser.triggered.connect(self.copyText)

        delUser = QAction(QIcon('icons/delete.png'),u'delete',self)
        delUser.triggered.connect(self.delTextItem)

        menu = QMenu()
        menu.addAction(editUser)
        menu.addAction(delUser)
        menu.exec_(QCursor.pos())
        e.accept()

    def copyText(self,b):
        # print 'msg copyed'
        cb = QApplication.clipboard()
        cb.setText(self.text)
        
    def delTextItem(self,b):
        # print 'msg deleted'
        self.listView.takeItem(self.listView.indexFromItem(self.listItem).row())

class TextItem(QtGui.QWidget):
    def __init__(self, listItem, listView, text = DEFAULT_MSG, lr=True):
        super(TextItem,self).__init__()
        hbox = QtGui.QHBoxLayout()
        text = BubbleTextMsg(listItem,listView,text,lr)

        if lr is not True:

            hbox.addSpacerItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
            hbox.addWidget(text)
        else:
            hbox.addWidget(text)
            hbox.addSpacerItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))

        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)
        self.setContentsMargins(0,0,0,0)
