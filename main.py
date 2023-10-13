from PyQt6 import QtCore, QtGui, QtWidgets
import psutil
import os
import sys

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setEnabled(True)
        main_window.resize(707, 260)
        main_window.setMinimumSize(QtCore.QSize(707, 260))
        main_window.setMaximumSize(QtCore.QSize(707, 260))
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(200, 180, 121, 41))
        self.start_button.setObjectName("start_button")
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setGeometry(QtCore.QRect(380, 180, 121, 41))
        self.ok_button.setObjectName("ok_button")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 691, 141))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setHtml('<p>Click on the "start Test" button to start the test</p>')
        main_window.setCentralWidget(self.centralwidget)
        self.ok_button.setEnabled(False)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.start_button.clicked.connect(self.run_test)
        self.ok_button.clicked.connect(QtWidgets.QMainWindow.close)
        

    def run_test(self):
        ram_check = self.check_ram()
        cpu_check = self.check_cpu()
        desktop_check = self.check_desktop()
        session_check = self.check_session()

        text = f"<p>{ram_check}</p><p>{cpu_check}</p><p>{desktop_check}</p><p>{session_check}</p>"

        self.textBrowser.setHtml(text)
        self.ok_button.setEnabled(True)

    def check_ram(self):
        ram = psutil.virtual_memory().total / (1024 ** 3) # Convert bytes to GB
        ram = round(ram)
        if ram >= 4:
            return "RAM: OK ({:.2f} GB)".format(ram)
        
        else:
            return "RAM: NOT OK ({:.2f} GB)".format(ram)

    def check_cpu(self):
        cpuinfo = open('/proc/cpuinfo').read()
        if 'sse4_1' in cpuinfo:
            return "CPU: OK (SSE4.1)"
        
        else:
            return "CPU: NOT OK (No SSE4.1)"

    def check_desktop(self):
        desktop_info = os.environ.get('DESKTOP_SESSION')
        if desktop_info and (desktop_info.startswith('gnome') or desktop_info.startswith('plasma')):
            return "Desktop: OK ({})".format(desktop_info)
        
        else:
            return "Desktop: NOT OK ({})".format(desktop_info)

    def check_session(self):
        session_info = os.environ.get('WAYLAND_DISPLAY')
        if session_info:
            return "Wayland: OK ({})".format(session_info)
        
        else:
            return "Wayland: unavailable"


    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Parch Linux Waydroid System Check"))
        self.start_button.setText(_translate("main_window", "Start Test"))
        self.ok_button.setText(_translate("main_window", "OK"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())
