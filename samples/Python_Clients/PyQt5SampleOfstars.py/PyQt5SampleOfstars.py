#-------------------------------------------------------------------------------
# Name:        PyQt5SampleOfstars.py
# Purpose:     Sample program of stars python with PyQt5
#
# Author:      Y.Nagatani
#
# Created:     2017-02-22
#-------------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit)
import stars

#-------------------------------------------------
# STARS code (QThread for STARS callback)
#-------------------------------------------------
class _QtThreadSTARSCallbak(QtCore.QThread):
    # Create the signal
    sigrecv = QtCore.pyqtSignal(str)
    siglogdisp = QtCore.pyqtSignal(str)

    def __init__(self,  parent, stars):
        super(_QtThreadSTARSCallbak, self).__init__(parent)
        self.stars = stars
        # Connect signal to the desired function
        self.sigrecv.connect(parent.RecvSTARSMessage)
        self.siglogdisp.connect(parent.LogUpdate)

    def run(self):
        self.stars._callbackrunning = True
        while self.stars._callbackrunning:
            mesg = self.stars.receive(None)
            # If STARS Command message arriving, do nothing for Qt in this case.
            self._cb_handler(mesg)
            if rt == '':
                self.stars._callbackrunning = False
        self.stars.disconnect()

    # Callback function for STARS message
    def _cb_handler(self,mess):
        global st
        try:
            sys.stdout.write('**Callback cb_handler(%s).**\n'%(mess))
            #!!Fatal error
            if mess == '':
                # Stop callback loop
                self.stars._callbackrunning = False
                # Send signal for STARS Reply message
                self.sigrecv.emit('!!cb_handler() got ' + st.getlasterrortext())
                sys.stdout.write('!!cb_handler() got ' + st.getlasterrortext() + '\n')
                return
        except:
            return

        #Reply message
        if(mess.command.startswith('@')):
            # Send signal for STARS Reply message
            self.sigrecv.emit(mess)
            return

        #Event message
        if(mess.command.startswith('_')):
            self.siglogdisp.emit(mess)
            return

        #Command message
        sendstr=''
        self.siglogdisp.emit(mess)
        if(mess.nodeto == st.nodename):
            if mess.message == 'hello':
                sendstr="@hello nice to meet you."
            elif mess.message == 'help':
                sendstr="@help hello help"
            else:
                sendstr='@' + mess.message + " Er: Bad command or parameter."
            st.send(mess.nodefrom,sendstr)
            self.siglogdisp.emit(st.nodename + '>' + mess.nodefrom + ' ' + sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')
        else:
            to=mess.nodeto.replace(st.nodename+'.','')
            sendstr='@' + mess.message + " Er: %s is down."%(to)
            st.send(st.nodename, mess.nodefrom, sendstr)
            self.siglogdisp.emit(st.nodename + '>' + mess.nodefrom + ' ' + sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')
        return

class MainWindow(QWidget):
    def __init__(self, parent=None):
        global st

        super(MainWindow, self).__init__(parent)

        self.inputLine = QLineEdit()
        self.inputLine.setText('System gettime')

        self.outputLine = QLineEdit()
        self.outputLine.setReadOnly(True)

        self.logOutput = QTextEdit()
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)

        self.sendButton = QPushButton("&Send")
        self.sendButton.clicked.connect(self.SendSTARSMessage)

        self.logclearButton = QPushButton("&Clear log")
        self.logclearButton.clicked.connect(self.ClearLog)

        self.logstopupdateButton = QPushButton("&Pause log update")
        self.logstopupdateButton.clicked.connect(self.StopLogUpdate)
        self.logstopupdate=True

        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("STARS command"), 0, 0)
        lineLayout.addWidget(self.inputLine, 0, 1)
        lineLayout.addWidget(self.sendButton, 0, 2)
        lineLayout.addWidget(QLabel("STARS last reply"), 1, 0)
        lineLayout.addWidget(self.outputLine, 1, 1)
        lineLayout.addWidget(QLabel("STARS message log"), 2, 0)
        lineLayout.addWidget(self.logOutput, 2, 1)

        LogButtonLayOut= QGridLayout()
        LogButtonLayOut.addWidget(self.logstopupdateButton,0,0)
        LogButtonLayOut.addWidget(self.logclearButton,1,0)
        lineLayout.addLayout(LogButtonLayOut,2,2)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(lineLayout)
        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle("Sample program of PyQt5 with STARS Python")

        #-------------------------------------------------
        # STARS code (START QThread for STARS callback)
        #-------------------------------------------------
        self.qthread = _QtThreadSTARSCallbak(self, st)
        self.qthread.start()

    #-------------------------------------------------
    # These functions will be called intenally.
    #-------------------------------------------------
    def ClearLog(self):
        self.logOutput.setText('')

    def StopLogUpdate(self):
        if(self.logstopupdate==True):
            self.logstopupdate=False
            self.logstopupdateButton.setText("&Resume log update")
        else:
            self.logstopupdate=True
            self.logstopupdateButton.setText("&Pause log update")

    def SendSTARSMessage(self):
        global st
        mesgstr = self.inputLine.text().strip()
        if(mesgstr != ''):
            rt=st.send(mesgstr)
            self.LogUpdate(mesgstr)
            if(rt == False):
                self.outputLine.setText('')
                self.logOutput.append(st.getlasterrortext())

    #-------------------------------------------------
    # These functions will be called from Qthread
    #-------------------------------------------------
    def LogUpdate(self,mesgstr):
        if(self.logstopupdate==True):
            buf=self.logOutput.toPlainText().split('\n')
            if(len(buf)>=50):
                buf=buf[1:]
                self.logOutput.setText('\n'.join(buf))
            self.logOutput.append(mesgstr)

    def RecvSTARSMessage(self,mesgstr):
        if(mesgstr!= ''):
            self.outputLine.setText(mesgstr)
            self.LogUpdate(mesgstr)

if __name__ == '__main__':
    import sys

    #----------------------------
    # STARS code (Main)--> START
    #----------------------------
    # Create stars instance
    starshost = 'localhost'
    starsnode1= 'samplepyclient';
    st = stars.StarsInterface(starsnode1, starshost)
    # Connect to STARS server
    st.setdebug(True)
    rt=st.connect()
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)
    #----------------------------
    # STARS code (Main)--> End
    #----------------------------

    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
