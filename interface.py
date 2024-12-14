import sys
import cv2
import serial
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class MySideBar(QMainWindow):
    def __init__(self):
        super(MySideBar, self).__init__()
        uic.loadUi('sidebar.ui', self)
        self.setWindowTitle("SideBar Menu")

        # Initialize camera and laser connection
        self.cap = None
        self.laser = None

        # Connect buttons to their respective functions
        self.pushButton_2.clicked.connect(self.page)
        self.pushButton.clicked.connect(self.page_2)
        self.pushButton_3.clicked.connect(self.page_3)
        self.pushButton_6.clicked.connect(self.page_4)
        
        # Connect buttons for camera and laser functions
        self.pushButton_10.clicked.connect(self.start_camera)
        self.pushButton_11.clicked.connect(self.stop_camera)
        self.pushButton_12.clicked.connect(self.connect_laser)
        self.pushButton_13.clicked.connect(self.disconnect_laser)
        self.pushButton_14.clicked.connect(self.toggle_laser)

    def page(self):
        self.stackedWidget.setCurrentIndex(0)

    def page_2(self):
        self.stackedWidget.setCurrentIndex(1)

    def page_3(self):
        self.stackedWidget.setCurrentIndex(2)

    def page_4(self):
        self.stackedWidget.setCurrentIndex(3)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)  
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def stop_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()

    def connect_laser(self):
        try:
            self.laser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  
        except serial.SerialException as e:
            print(f"Failed to connect to laser: {e}")

    def disconnect_laser(self):
        if self.laser and self.laser.is_open:
            self.laser.close()

    def toggle_laser(self):
        if self.laser and self.laser.is_open:
            self.laser.write(b'TOGGLE\n')  
with actual command

    def closeEvent(self, event):
        self.stop_camera()
        self.disconnect_laser()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySideBar()
    window.show()
    sys.exit(app.exec_())
