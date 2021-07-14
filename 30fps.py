from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sys
import config
import fpstimer

timer = fpstimer.FPSTimer(60)

class MainWindow(QMainWindow, QDialog):
    def __init__(self): #khi ép object vô class thì luôn chạy hàm constructor này
        super(MainWindow, self).__init__()
        self.initUI() #khi chạy sẽ gọi hàm initUI

    def initUI(self): #set các thông số của cửa sổ game
        self.setGeometry(0, 0, 1920, 1080) #kích thước fullHD
        self.setWindowTitle("Game cua Nghi")
        self.startup() #gọi hàm startup
        self.showMaximized() #để phóng to fullscreen cửa sổ game

    def startup(self):
        global timer
        self.background=QLabel(self) #xem QLabel như là 1 cái khuôn nhỏ khác, ép object background vào
        self.background.setScaledContents(True)
        self.background.setPixmap(QPixmap(config.background)) #set hình cho object tên là background
        self.background.setGeometry(0,0, 1920, 1080)#set vị trí và kích thước, 0-0 là góc trái trên cùng, fullHD
        self.background.show()

        self.target=QLabel(self)
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.setGeometry(0, 400, 180, 270)
        self.target.show()

        '''
        for i in range(0, 1920):
            self.target.move(i, 500) #di chuyển đến tọa độ x y trên màn hình
            self.target.show() #hiện hình mèo ở vị trí đã di chuyển đến
            time.sleep(0.1)
            timer.sleep()
            pass
            '''

app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show()
sys.exit(app.exec_()) #syntax mặc định