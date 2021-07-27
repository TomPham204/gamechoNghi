#PyQt5 là thư viện hỗ trợ làm UI. Khi kết hợp với code logic [if else vòng lặp] thì sẽ thành game
#config là 1 file chứa các đường dẫn của tài nguyên được game sử dụng
#sys là cái để chạy, để thoát
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from playsound import playsound
import sys
import config
import random
import winsound

hasSound=False #nếu muốn có âm thanh khi bắn thì thay False bằng True nhưng khi bắn sẽ bị khựng. Không import module ray chỉ để chạy song song duy nhất 2 method vì quá nặng!

class MainWindow(QMainWindow, QDialog): #class MainWindow là cái khuôn
    def __init__(self): #khi ép object vô class thì luôn chạy hàm constructor này
        super(MainWindow, self).__init__()
        self.x_pos=1 #vị trí ban đầu của con mèo trên trục x
        self.setGeometry(0, 0, 1920, 1080) #kích thước fullHD=full screen
        self.setWindowTitle("Shoot the pussy") #cái dòng góc trên bên trái của cửa sổ >> tên của cửa sổ đang chạy
        #self.showMaximized() #để phóng to fullscreen cửa sổ game
        self.count = random.randint(2, 5) #random số đạn
        self.start() #gọi hàm start

    def start(self): #khi gọi hàm start thì lần lượt chạy các method ở dưới
        self.timer=QTimer(self) #animation object hỗ trợ con mèo chuyển động qua phải
        self.timer.timeout.connect(self.moveTarget) #object sẽ đếm, khi hết thời gian của 1 frame thì sẽ gọi hàm moveTarget để di chuyển con mèo qua phải

        self.miss_timer=QTimer(self) #animation object cho bắn hụt
        self.miss_timer.timeout.connect(self.missFireHide)

        self.runGame() #gọi hàm runGame
        self.show() #hiện mọi object đang có

    def runGame(self):   
        winsound.PlaySound("bgm.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ) #background music
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

        self.amuCount=QLabel(self) #hiển thị số đạn còn lại
        self.amuCount.setScaledContents(True)
        self.amuCount.setText(str(self.count))
        self.amuCount.setFont(QFont("Times", 20))
        self.amuCount.setStyleSheet("background-color: white")
        self.amuCount.setGeometry(self.gun.x()+105, self.gun.y()+160, 25, 40)
        self.amuCount.show()

        self.target=QLabel(self) #hình con mèo làm mục tiêu bị bắn
        self.target.setScaledContents(True)
        self.target.setPixmap(QPixmap(config.target)) #set hình mèo
        self.target.setGeometry(0, 350, 180, 110)
        self.target.show()

        self.mid=QLabel(self) #crosshair, cái vòng đỏ đỏ để ngắm bắn
        self.mid.setScaledContents(True)
        self.mid.setPixmap(QPixmap(config.mid)) #set hình
        self.mid.setGeometry(865, 320, 200, 200)
        self.mid.show()

        self.timer.start(int((800-self.count*80)/45)) #chạy object timer để bắt đầu di chuyển con mèo qua phải, tốc độ nhanh chậm tỉ lệ với số đạn của súng

    def mousePressEvent(self, event):
        global hasSound
        _x = self.target.x() #lấy tọa độ x của con mèo tại thời điểm click chuột
        if event.button() == Qt.LeftButton: #nếu click chuột trái trong khi...
            if(self.count > 0):
                self.count -= 1 #bắn mất 1 viên nên -1
                self.amuCount.setText(str(self.count)) #set text của ô hiện số đạn thành n-1

                if(hasSound==True): #không có tiếng bắn nếu has sound=false
                    playsound('fire.mp3')

                if(_x < self.mid.x() + 75 and _x > self.mid.x() - 50): #Xac dinh coi con mèo nằm trong tầm bắn khong 
                    self.noticeWin() #gọi hàm để thông báo đã giết mèo và thắng
                elif(_x>1920): #... con mèo ngoài tầm bắn và đã ra khỏi màn hình
                    self.noticeLose()
                    sys.exit() #nếu mèo chạy ra khỏi màn hình thì thua, quit game
                else: #... mèo ngoài tầm bắn nhưng vẫn còn trong màn hình
                    self.missFire()
                    self.miss_timer.start(int(990/3))
                    pass

            if(self.count == 0):
                #sys.exit()
                pass

    def missFire(self):
        self.miss=QLabel(self) #nếu mèo còn trong màn hình nhưng không nằm trong tầm bắn thì hiện bắn hụt
        self.miss.setScaledContents(True)
        self.miss.setPixmap(QPixmap(config.miss))
        self.miss.setGeometry(self.mid.x()+20, 350, 160, 145)
        self.miss.show()
    
    def missFireHide(self):
        self.miss.hide()

    def moveTarget(self): #hàm để di chuyển con mèo, mèo là target=mục tiêu bị bắn
        self.target.move(self.x_pos, 350) #di chuyển mèo qua phải
        self.target.show()
        self.x_pos+=4

    def noticeWin(self):
        self.timer.stop() #khi đã bắn trúng thì dừng hình mèo lại không cho di chuyển
        #self.target.hide()
        winsound.PlaySound(None, winsound.SND_ASYNC) #tắt nhạc bgm

        self.killed=QLabel(self) #hiện hình đã bắn trúng
        self.killed.setScaledContents(True)
        self.killed.setPixmap(QPixmap(config.killed)) #set hình đã bắn trúng
        self.killed.setGeometry(self.mid.x()+45, 375, 105, 110)
        self.killed.show()

        self.notice=QMessageBox(self, text="Congratulations,You win") #hiện cái pop up you win
        self.notice.move(850, 100)
        self.notice.show()
        self.notice.buttonClicked.connect(sys.exit) #khi click nút ok thì sẽ thoát gamedef noticeWin(self):

    def noticeLose(self):
        self.timer.stop() #dừng hình mèo lại không cho di chuyển
        #self.target.hide()
        winsound.PlaySound(None, winsound.SND_ASYNC)

        self.notice=QMessageBox(self, text="Better luck next time :< ") #hiện cái text box
        self.notice.move(850, 100)
        self.notice.show()
        self.notice.buttonClicked.connect(sys.exit) #khi click nút ok thì sẽ thoát game


    def keyPressEvent(self, event):
        x_gun = self.gun.x()
        if event.key() == Qt.Key_Left:
            if x_gun > 0:
                self.gun.move(x_gun - 10, 820)
                self.amuCount.move(self.gun.x()+105, self.gun.y()+160)
                self.mid.move(x_gun + 4, self.mid.y())
            if x_gun>=1920:
                sys.exit()

        elif event.key() == Qt.Key_Right:
            if x_gun < 1920:
                self.gun.move(x_gun + 10, 820)
                self.amuCount.move(self.gun.x()+105, self.gun.y()+160)
                self.mid.move(x_gun + 25, self.mid.y())
            if x_gun>=1920:
                sys.exit()


app=QApplication(sys.argv) #syntax mặc định của thư viện pyqt5 hỗ trợ tạo giao diện
window=MainWindow() #object window ép vô khuôn(class MainWindow)
window.show() #hiện cửa sổ game
sys.exit(app.exec_()) #syntax mặc định để chạy