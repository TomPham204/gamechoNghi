#PyQt5 là thư viện hỗ trợ làm UI. Khi kết hợp với code logic [if else vòng lặp] thì sẽ thành game
#config là 1 file chứa các đường dẫn của tài nguyên được game sử dụng
#sys là cái để chạy, để thoát
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import config

class MainWindow(QMainWindow, QDialog): #class MainWindow là cái khuôn
    def __init__(self): #khi ép object vô class thì luôn chạy hàm constructor này
        super(MainWindow, self).__init__()
        self.x_pos=1 #vị trí ban đầu của con mèo trên trục x
        self.setGeometry(0, 0, 1920, 1080) #kích thước fullHD
        self.setWindowTitle("Game cua Nghi") #cái dòng góc trên bên trái của cửa sổ >> tên của cửa sổ đang chạy
        self.showMaximized() #để phóng to fullscreen cửa sổ game
        self.start() #gọi hàm start

    def start(self): #khi gọi hàm start thì lần lượt chạy các method ở dưới
        self.timer=QTimer(self) #animation object hỗ trợ con mèo chuyển động qua phải
        self.timer.timeout.connect(self.moveTarget) #object sẽ đếm, khi hết thời gian của 1 frame thì sẽ gọi hàm moveTarget để di chuyển con mèo qua phải
        self.runGame() #gọi hàm runGame
        self.show() #hiện mọi object đang có

    def runGame(self):   
        self.background=QLabel(self) #xem QLabel như là 1 cái khuôn nhỏ khác, ép object background vào
        self.background.setScaledContents(True) #scale hình khi phóng to thu nhỏ cửa sổ
        self.background.setPixmap(QPixmap(config.background)) #set hình cho object tên là background
        self.background.setGeometry(0,0, 1920, 1080)#set vị trí và kích thước, 0-0 là góc trái trên cùng, fullHD
        self.background.show()

        self.gun=QLabel(self) #hình cái súng ở giữa đáy màn hình
        self.gun.setScaledContents(True)
        self.gun.setPixmap(QPixmap(config.gun)) #set hình súng bắn mèo
        self.gun.move(847, 820) #set vị trí
        self.gun.resize(230, 215) #set kích thước
        self.gun.show()

        self.target=QLabel(self) #hình con mèo làm mục tiêu bị bắn
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.setGeometry(0, 350, 180, 110)
        self.target.show()

        self.mid=QLabel(self) #crosshair, cái vòng đỏ đỏ để ngắm bắn
        self.mid.setScaledContents(True)
        self.mid.setPixmap(QPixmap(config.mid)) #set hình
        self.mid.setGeometry(865, 330, 200, 200)
        self.mid.show()

        self.timer.start(500/45) #chạy object timer để bắt đầu di chuyển con mèo qua phải

    def mousePressEvent(self, event):
        _x = self.target.x() #lấy tọa độ x của con mèo tại thời điểm click chuột
        if event.button() == Qt.LeftButton: #nếu click chuột trái trong khi...
            if(_x < 900 and _x > 790): #... con mèo nằm trong tầm bắn
                self.noticeWin() #gọi hàm để thông báo đã giết mèo và thắng
            elif(_x>1920): #... con mèo ngoài tầm bắn và đã ra khỏi màn hình
                sys.exit() #nếu mèo chạy ra khỏi màn hình thì thua, quit game
            else: #... mèo ngoài tầm bắn nhưng vẫn còn trong màn hình
                self.miss=QLabel(self) #nếu mèo còn trong màn hình nhưng không nằm trong tầm bắn thì hiện bắn hụt
                self.miss.setScaledContents(True)
                self.miss.setPixmap(QPixmap(config.miss))
                self.miss.setGeometry(self.target.x()+10, 350, 160, 145)
                self.miss.show()

    def moveTarget(self): #hàm để di chuyển con mèo, mèo là target=mục tiêu bị bắn
        self.target.move(self.x_pos, 350) #di chuyển mèo qua phải
        self.target.show()
        self.x_pos+=2

    def noticeWin(self):
        self.timer.stop() #khi đã bắn trúng thì dừng hình mèo lại không cho di chuyển
        #self.target.hide()

        self.killed=QLabel(self) #hiện hình đã bắn trúng
        self.killed.setScaledContents(True)
        self.killed.setPixmap(QPixmap(config.killed)) #set hình đã bắn trúng
        self.killed.setGeometry(self.target.x()+20, 350, 145, 150)
        self.killed.show()

        self.notice=QMessageBox(self, text="You win") #hiện cái pop up you win
        self.notice.move(850, 100)
        self.notice.show()
        self.notice.buttonClicked.connect(sys.exit) #khi click nút ok thì sẽ thoát game


app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show() #hiện cửa sổ game
sys.exit(app.exec_()) #syntax mặc định để chạy