from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import keyboard
import config

class MainWindow(QMainWindow, QDialog):
    def __init__(self): #khi ép object vô class thì luôn chạy hàm constructor này
        super(MainWindow, self).__init__()
        self.x_pos=1
        self.setGeometry(0, 0, 1920, 1080) #kích thước fullHD
        self.setWindowTitle("Game cua Nghi")
        self.showMaximized() #để phóng to fullscreen cửa sổ game
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.moveTarget)
        self.runGame()
        self.show()

    def runGame(self):   
        self.background=QLabel(self) #xem QLabel như là 1 cái khuôn nhỏ khác, ép object background vào
        self.background.setScaledContents(True)
        self.background.setPixmap(QPixmap(config.background)) #set hình cho object tên là background
        self.background.setGeometry(0,0, 1920, 1080)#set vị trí và kích thước, 0-0 là góc trái trên cùng, fullHD
        self.background.show()

        self.gun=QLabel(self)
        self.gun.setScaledContents(True)
        self.gun.setPixmap(QPixmap(config.gun)) #set hình súng bắn mèo
        self.gun.move(847, 820) #set vị trí
        self.gun.resize(230, 215)
        self.gun.show()

        self.target=QLabel(self)
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.setGeometry(0, 350, 180, 245)
        self.target.show()

        self.timer.start(500/45)

    def mousePressEvent(self, event):
        _x = self.target.x()
        _y = self.target.y()
        if event.button() == Qt.LeftButton:
            if(_x < 900 and _x > 790):
                self.noticeWin()
            elif (_x >1920):
                #self.hide()
                #self.startup()
                pass
            else:
                pass

    def moveTarget(self):
        self.target.move(self.x_pos, 350)
        self.target.show()
        self.x_pos+=2

    def noticeWin(self):
        self.timer.stop()
        self.target.hide()

        self.killed=QLabel(self)
        self.killed.setScaledContents(True)
        self.killed.setPixmap(QPixmap(config.killed)) #set hình đã bắn trúng
        self.killed.setGeometry(self.target.x(), 350, 220, 245)
        self.killed.show()

        self.notice=QMessageBox(self, text="You win") #hiện cái pop up you win
        self.notice.move(850, 100)
        self.notice.show()


app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show()
sys.exit(app.exec_()) #syntax mặc định