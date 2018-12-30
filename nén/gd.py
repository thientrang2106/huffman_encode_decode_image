# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
import os, time
from lzw import *
from huffmanNew import *


class Ui_GUI(object):
    _fileName =""

    def setupUi(self, GUI):
        GUI.setObjectName("GUI")
        GUI.resize(341, 350)
        GUI.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(GUI)
        self.centralwidget.setObjectName("centralwidget")

        self._method = QtWidgets.QComboBox(self.centralwidget)
        self._method.setGeometry(QtCore.QRect(60, 50, 181, 21))
        self._method.setObjectName("_method")
        self._method.addItem("")
        self._method.addItem("")
        self._method.addItem("")
        self._method.addItem("")

        self._url = QtWidgets.QLineEdit(self.centralwidget)
        self._url.setEnabled(True)
        self._url.setGeometry(QtCore.QRect(60, 20, 181, 21))
        self._url.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self._url.setMouseTracking(False)
        self._url.setAcceptDrops(False)
        self._url.setObjectName("_url")
        self._url.setReadOnly(True)

        self._decom = QtWidgets.QPushButton(self.centralwidget)
        self._decom.setGeometry(QtCore.QRect(200, 90, 51, 31))
        self._decom.setMouseTracking(False)
        self._decom.setAutoFillBackground(True)
        self._decom.setDefault(True)
        self._decom.setFlat(False)
        self._decom.setObjectName("_decom")

        self._showtext = QtWidgets.QTextBrowser(self.centralwidget)
        self._showtext.setGeometry(QtCore.QRect(60, 150, 231, 100))
        self._showtext.setObjectName("_showtext")

        self._com = QtWidgets.QPushButton(self.centralwidget)
        self._com.setGeometry(QtCore.QRect(100, 90, 51, 31))
        self._com.setAutoDefault(False)
        self._com.setDefault(True)
        self._com.setObjectName("_com")

        self._browse = QtWidgets.QPushButton(self.centralwidget)
        self._browse.setGeometry(QtCore.QRect(260, 20, 51, 21))
        self._browse.setMouseTracking(False)
        self._browse.setAutoFillBackground(True)
        self._browse.setDefault(True)
        self._browse.setFlat(False)
        self._browse.setObjectName("_browse")

        GUI.setCentralWidget(self.centralwidget)

        self._menubar = QtWidgets.QMenuBar(GUI)
        self._menubar.setGeometry(QtCore.QRect(0, 0, 341, 21))
        self._menubar.setObjectName("_menubar")
        self._menuAbout = QtWidgets.QMenu(self._menubar)
        self._menuAbout.setObjectName("_menuAbout")
        GUI.setMenuBar(self._menubar)
    
        
        self._menubar.addAction(self._menuAbout.menuAction())

        self._Authors = QtWidgets.QAction(GUI)
        self._Authors.setObjectName("_Authors")
        self._menuAbout.addAction(self._Authors)
        self._menubar.addAction(self._menuAbout.menuAction())

        self._statusbar = QtWidgets.QStatusBar(GUI)
        self._statusbar.setObjectName("_statusbar")
        GUI.setStatusBar(self._statusbar)
        self._statusbar.showMessage('Ready')

        self.retranslateUi(GUI)
        self._menubar.triggered.connect(self._aboutSlot)
        self._browse.clicked.connect(self._browseSlot)
        self._decom.clicked.connect(self._decompressSlot)
        self._com.clicked.connect(self._compressSlot)
        self._url.returnPressed.connect(self._geturlSlot)
        self._method.currentIndexChanged['int'].connect(self._getmethodSlot)
        QtCore.QMetaObject.connectSlotsByName(GUI)



    def retranslateUi(self, GUI):
        
        _translate = QtCore.QCoreApplication.translate
        GUI.setWindowTitle(_translate("GUI", "Compression Demo"))
        self._method.setItemText(0, _translate("GUI", "Chọn thuật toán nén ảnh"))
        self._method.setItemText(1, _translate("GUI", "Huffman"))
        self._method.setItemText(2, _translate("GUI", "LZW"))
        self._method.setItemText(3, _translate("GUI", "JPEG Standard"))
        self._url.setText(_translate("GUI", "Chọn đường dẫn"))
        self._decom.setText(_translate("GUI", "Giải nén"))
        self._com.setText(_translate("GUI", "Nén"))
        self._browse.setText(_translate("GUI", "Chọn"))
        self._menuAbout.setTitle(_translate("GUI", "About"))
        self._Authors.setText(_translate("GUI", "Authors"))
    
  
    def isValid(fileName ):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try: 
            file = open( fileName, 'r' )
            file.close()
            return True
        except:
            return False


    def _geturlSlot( self ):
        ''' Called when the user enters a string in the _url and
        presses the ENTER key.
        '''
        pass

    def _aboutSlot( self ):
        ''' Called when the user click About
        '''
        QtWidgets.QMessageBox.about(self.centralwidget, 'About','---Nhóm N---\n Nguyễn Văn Minh              - 15520488\n Trần Nguyên Khánh           - 15520363\n Nguyễn Trọng Nhân          - 15520570\n Huỳnh Ngọc Thiên Trang - 15520917')
    
        pass

    def _browseSlot(self):
        ''' Called when the user presses the _browse
        '''
        self._statusbar.showMessage('Ready')
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)

        if Ui_GUI.isValid(fileName):
            self._url.setText(fileName)
            print("FILE NAME======================",fileName)        
        else: 
            print("CHƯA CHỌN ĐƯỜNG DẪN============")
        pass

    def _getmethodSlot(self):
        ''' Call when click and choose in the _method
        '''        
        self._statusbar.showMessage('Ready')
        print("METHOD======================",self._method.currentText(), ':',self._method.currentIndex())
        pass

    def _compressSlot(self):
        ''' Call when click and choose in the _nén
        '''
        self._showtext.clear()        

        if self._method.currentIndex() == 1: #Nén Huffman
            self._statusbar.showMessage('Đang nén...')
            print("COMPRESSING BY HUFFMAN======================",self._url.text())
            start_time = time.time()
            file2 = hm_compression(self._url.text())
            end_time = time.time()
            total_time = round((end_time - start_time),4)
            file1 = file2.replace("_hm.bin","")            
            self.Show_Text_Com(file1,file2,total_time)
            print("DONE HUFFMAN======================")
            self._statusbar.showMessage('Hoàn tất!')
        
        if self._method.currentIndex() == 2: #Nén LZW
            self._statusbar.showMessage('Đang nén...')
            print("COMPRESSING BY LZW======================",self._url.text())
            start_time = time.time()
            file2 = lzw_compression(self._url.text())
            end_time = time.time()
            total_time = round((end_time - start_time),4)
            file1 = file2.replace("_lzw.bin","")            
            self.Show_Text_Com(file1,file2,total_time)
            print("DONE LZW======================")
            self._statusbar.showMessage('Hoàn tất!')
        
        pass

    def _decompressSlot(self):
        self._showtext.reload()
        if self.get_filename(self._url.text()).find('.bin') == -1 :
            QtWidgets.QMessageBox.warning(self.centralwidget,'Lỗi','Vui lòng chọn file .bin')
    
        if self._method.currentIndex() == 1: #Nén Huffman
            self._statusbar.showMessage('Đang giải nén...')
            print("DECOMPRESSING BY HUFFMAN======================",self._url.text())
            start_time = time.time()
            file1 = hm_decompression(self._url.text())
            end_time = time.time()
            total_time = round((end_time - start_time),4)
            self.Show_Text_Decom(file1,total_time)
            print("DONE HUFFMAN======================")
            self._statusbar.showMessage('Hoàn tất!')


        if self._method.currentIndex() == 2: #Nén LZW
            self._statusbar.showMessage('Đang giải nén...')
            print("DECOMPRESSING BY LZW======================",self._url.text())
            start_time = time.time()
            file1 = lzw_decompression(self._url.text())
            end_time = time.time()
            total_time = round((end_time - start_time),4)
            self.Show_Text_Decom(file1,total_time)
            print("DONE LZW======================")
            self._statusbar.showMessage('Hoàn tất!')

        pass


    def Show_Text_Com(self, file1, file2, total_time):
        self._showtext.clear()
        x1 = os.path.getsize(file1)
        x2 = os.path.getsize(file2)
        st = '- Kích thước ảnh ban đầu: ' + str(x1) +' bytes' + '\n- Kích thước file nén: ' + str(x2) +' bytes'+ '\n- Hiệu suất nén: ' + str(round(((x1-x2)/x1)*100,4)) + '%' + '\n- Thời gian nén: ' + str(total_time) + 's'+ '\nTên file nén: ' + self.get_filename(file2)
        self._showtext.setText(st)
        
    def Show_Text_Decom(self, file1,total_time):
        self._showtext.clear()
        st = self.get_filename(file1)
        self._showtext.setText("File ảnh sau khi giải nén: " + st + '\nThời gian giải nén: ' + str(total_time) + 's')

    def get_filename(self,url):
        st =""
        kq =""
        for i in range(len(url))[::-1]:
            if url[i] != '/':
                st += url[i]
            else:
                break
        for i in range(len(st))[::-1]:
            kq += st[i]
        return kq



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())