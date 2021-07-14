from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
import ctypes
import keyboard
import config
import ray

ray.init() #ray hỗ trợ chạy song song nhiều method tại 1 thời điểm >> vừa detect click vừa move object trên màn hình

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
        self.background=QLabel(self) #xem QLabel như là 1 cái khuôn nhỏ khác, ép object background vào
        self.background.setScaledContents(True)
        self.background.setPixmap(QPixmap(config.background)) #set hình cho object tên là background
        self.background.setGeometry(0,0, 1920, 1080)#set vị trí và kích thước, 0-0 là góc trái trên cùng, fullHD
        self.background.show()

        self.instruct=QLabel(self) #textbox hướng dẫn chơi
        self.instruct.setText("Press Space to start")
        self.instruct.setScaledContents(True)
        self.instruct.setFont(QFont('Times', 16)) #set font, kích cỡ chữ
        self.instruct.setGeometry(830, 750, 300, 80)#set vị trí và kích thước
        self.instruct.setStyleSheet("background-color : #A9A9A9;")#set màu
        self.instruct.show()

        #keyboard.wait('Space') #đợi player, khi player nhấn Space thì sẽ chạy 2 dòng phía dưới aka bắt đầu game
        time.sleep(5)
        self.instruct.hide()
        self.runGame() #chạy hàm rungame

    def runGame(self):    
        self.gun=QLabel(self)
        self.gun.setScaledContents(True)
        self.gun.setPixmap(QPixmap(config.gun)) #set hình súng bắn mèo
        self.gun.move(940, 1000) #set vị trí
        self.gun.show()

        self.target=QLabel(self)
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.resize(36, 20) #set kích thước hình mèo

        self.x_pos = int(0) #con mèo bắt đầu chạy ngang từ x=0 ~ cạnh trái màn hình đến x=1080 ~ cạnh phải màn hình

        for i in range(0, 1920):
            self.result = ray.get([self.moveTarget.remote(i), self.detectClick.remote("L")]) #chạy song song, vừa detect click trong khi vẫn move target
            ray.close()
            print(self.result)
            time.sleep(0.03) #30fps, xuất 1 hình mỗi 0.03 giây >> 0.03*30 = 30 hình 1 giây
            self.x+=5 #tăng x để vòng lặp kế tiếp thì hình mèo di chuyển qua phải

            if(self.result==True):
                if(self.x>451 and self.x<629): #nếu đã click và con mèo nằm trong tầm bắn trúng aka giữa màn hình
                    self.isWin=True #set trạng thái là đã thắng
                    self.target.hide()

                    self.killed=QLabel(self)
                    self.killed.setScaledContents(True)
                    self.killed.setPixmap(QPixmap(config.killed)) #hiện hình đã bắn trúng
                    self.killed.resize(30, 30)
                    self.killed.move(self.x, self.y) #set vị trí hiện ở tọa độ lúc nhấn bắn
                    self.killed.show()
                    time.sleep(3)
                    break #thoát khỏi loop
            
            if(self.x>=1080): #nếu hình mèo chạy sát tới cạnh phải màn hình mà mình bắn hụt/không bắn
                self.isWin=False #thua
                break #thoát khỏi loop

        if self.isWin==True: #nếu trạng thái là thắng
            self.noticeWin() #thông báo chiến thắng
            time.sleep(3)
            #self.startup() #gọi lại hàm startup
        else: #nếu thua
            self.target.hide() #ẩn hình mèo
            #self.startup()

    @ray.remote
    def moveTarget(self, x_pos):
        self.target.hide()
        self.target.move(x_pos, 400) #di chuyển đến tọa độ x y trên màn hình
        self.target.show() #hiện hình mèo ở vị trí đã di chuyển đến

    def noticeWin(self):
        self.notice=QMessageBox(self, text="You win") #hiện cái pop up you win
        self.notice.show()

    @ray.remote
    def detectClick(self, button, watchtime = 20): #phức tạp, chỉ cần biết là dùng để detectClick, trả về true hoặc false
        if button in (1, '1', 'l', 'L', 'left', 'Left', 'LEFT'):
            self.bnum = 0x01
        elif button in (2, '2', 'r', 'R', 'right', 'Right', 'RIGHT'):
            self.bnum = 0x02
        start = time.time()
        while 1:
            if ctypes.windll.user32.GetKeyState(self.bnum) not in [0, 1]:
                return True
            elif time.time() - start >= watchtime:
                break
            time.sleep(0.001)
        return False


app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show()
sys.exit(app.exec_()) #syntax mặc định