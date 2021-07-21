from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sys
import config
import fpstimer
from pynput.keyboard import Key, Controller

timer = fpstimer.FPSTimer(120)
keyboard = Controller()

class MainWindow(QMainWindow, QDialog):
    def __init__(self): #khi ép object vô class thì luôn chạy hàm constructor này
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 1920, 1080) #kích thước fullHD
        self.setWindowTitle("Game cua Nghi")
        self.showMaximized() #để phóng to fullscreen cửa sổ game
        self.startup()
        self.runGame()
        self.show()

    def startup(self):
        self.background=QLabel(self) #xem QLabel như là 1 cái khuôn nhỏ khác, ép object background vào
        self.background.setScaledContents(True)
        self.background.setPixmap(QPixmap(config.background)) #set hình cho object tên là background
        self.background.setGeometry(0,0, 1920, 1080)#set vị trí và kích thước, 0-0 là góc trái trên cùng, fullHD
        self.background.show()

    def runGame(self):
        self.target=QLabel(self)
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.setGeometry(0, 350, 180, 245)
        self.target.show()

    def keyPressEvent(self, event):
        _x = self.target.x()
        _y = self.target.y()
        if event.key() == Qt.Key_Right:
                _x += 5
                self.target.move(_x, _y)

app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show()
sys.exit(app.exec_()) #syntax mặc định