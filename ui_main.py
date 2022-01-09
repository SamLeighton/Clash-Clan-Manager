# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 720)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Game Graphics/CCM logo circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
"    border-image: url(:/titleScreen/background image.png);\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.title_image = QtWidgets.QLabel(self.centralwidget)
        self.title_image.setGeometry(QtCore.QRect(170, -20, 691, 351))
        self.title_image.setMinimumSize(QtCore.QSize(0, 0))
        self.title_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.title_image.setAutoFillBackground(False)
        self.title_image.setStyleSheet("image: url(:/titleScreen/clash clan manager text.png);")
        self.title_image.setText("")
        self.title_image.setScaledContents(True)
        self.title_image.setAlignment(QtCore.Qt.AlignCenter)
        self.title_image.setObjectName("title_image")
        self.login_form = QtWidgets.QGroupBox(self.centralwidget)
        self.login_form.setGeometry(QtCore.QRect(300, 270, 451, 391))
        self.login_form.setAutoFillBackground(False)
        self.login_form.setStyleSheet("QGroupBox {\n"
"border: 2px solid gray;\n"
"border-color: #424242;\n"
"border-radius: 15px;\n"
"background-color: white\n"
"}")
        self.login_form.setTitle("")
        self.login_form.setObjectName("login_form")
        self.email_label_login = QtWidgets.QLabel(self.login_form)
        self.email_label_login.setGeometry(QtCore.QRect(20, 20, 211, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.email_label_login.setFont(font)
        self.email_label_login.setObjectName("email_label_login")
        self.email_entry_login = QtWidgets.QLineEdit(self.login_form)
        self.email_entry_login.setGeometry(QtCore.QRect(20, 90, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.email_entry_login.setFont(font)
        self.email_entry_login.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(222, 222, 222);\n"
"    border-radius: 7;\n"
"    border: 1px solid black\n"
"}")
        self.email_entry_login.setObjectName("email_entry_login")
        self.password_label_login = QtWidgets.QLabel(self.login_form)
        self.password_label_login.setGeometry(QtCore.QRect(20, 130, 211, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label_login.setFont(font)
        self.password_label_login.setObjectName("password_label_login")
        self.password_entry_login = QtWidgets.QLineEdit(self.login_form)
        self.password_entry_login.setGeometry(QtCore.QRect(20, 200, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.password_entry_login.setFont(font)
        self.password_entry_login.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(222, 222, 222);\n"
"    border-radius: 7;\n"
"    border: 1px solid black\n"
"}")
        self.password_entry_login.setObjectName("password_entry_login")
        self.login_close_button = QtWidgets.QPushButton(self.login_form)
        self.login_close_button.setGeometry(QtCore.QRect(400, 10, 41, 41))
        self.login_close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_close_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.login_close_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 6;\n"
"    image: url(:/titleScreen/closebutton.png);\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"\n"
"}")
        self.login_close_button.setText("")
        self.login_close_button.setIconSize(QtCore.QSize(40, 40))
        self.login_close_button.setObjectName("login_close_button")
        self.log_in_button_login = QtWidgets.QPushButton(self.login_form)
        self.log_in_button_login.setGeometry(QtCore.QRect(30, 290, 381, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.log_in_button_login.setFont(font)
        self.log_in_button_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.log_in_button_login.setAutoFillBackground(False)
        self.log_in_button_login.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0.125, y1:0.471909, x2:0.938, y2:0.472, stop:0         rgba(49, 87, 255, 255), stop:1 rgba(38, 168, 255, 255)); \n"
"    color: white;\n"
"     border-radius: 10; \n"
"    padding: 6; \n"
"    border-style: outset;\n"
"    border-width: 1;\n"
"    border-top-color: rgb(135, 135, 135);\n"
"    border-left-color: rgb(135, 135, 135);\n"
"    border-right-color: rgb(0, 0, 0);\n"
"    border-bottom-color: rgb(0, 0, 0);\n"
"    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: outset;\n"
"    border-top-color: rgb(0, 0, 0);\n"
"    border-left-color: rgb(0, 0, 0);\n"
"    border-right-color: rgb(135, 135, 135);\n"
"    border-bottom-color: rgb(135, 135, 135);\n"
"    \n"
"}")
        self.log_in_button_login.setCheckable(False)
        self.log_in_button_login.setChecked(False)
        self.log_in_button_login.setDefault(False)
        self.log_in_button_login.setFlat(False)
        self.log_in_button_login.setObjectName("log_in_button_login")
        self.login_failed = QtWidgets.QLabel(self.login_form)
        self.login_failed.setGeometry(QtCore.QRect(30, 260, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.login_failed.setFont(font)
        self.login_failed.setStyleSheet("color: red")
        self.login_failed.setAlignment(QtCore.Qt.AlignCenter)
        self.login_failed.setObjectName("login_failed")
        self.email_entry_login.raise_()
        self.password_label_login.raise_()
        self.password_entry_login.raise_()
        self.login_close_button.raise_()
        self.log_in_button_login.raise_()
        self.login_failed.raise_()
        self.email_label_login.raise_()
        self.log_in_button = QtWidgets.QPushButton(self.centralwidget)
        self.log_in_button.setGeometry(QtCore.QRect(340, 340, 381, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.log_in_button.setFont(font)
        self.log_in_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.log_in_button.setAutoFillBackground(False)
        self.log_in_button.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0.125, y1:0.471909, x2:0.938, y2:0.472, stop:0         rgba(49, 87, 255, 255), stop:1 rgba(38, 168, 255, 255)); \n"
"    color: white;\n"
"     border-radius: 10; \n"
"    padding: 6; \n"
"    border-style: outset;\n"
"    border-width: 1;\n"
"    border-top-color: rgb(135, 135, 135);\n"
"    border-left-color: rgb(135, 135, 135);\n"
"    border-right-color: rgb(0, 0, 0);\n"
"    border-bottom-color: rgb(0, 0, 0);\n"
"    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: outset;\n"
"    border-top-color: rgb(0, 0, 0);\n"
"    border-left-color: rgb(0, 0, 0);\n"
"    border-right-color: rgb(135, 135, 135);\n"
"    border-bottom-color: rgb(135, 135, 135);\n"
"    \n"
"}")
        self.log_in_button.setCheckable(False)
        self.log_in_button.setChecked(False)
        self.log_in_button.setDefault(False)
        self.log_in_button.setFlat(False)
        self.log_in_button.setObjectName("log_in_button")
        self.signup_form = QtWidgets.QGroupBox(self.centralwidget)
        self.signup_form.setGeometry(QtCore.QRect(300, 270, 451, 391))
        self.signup_form.setAutoFillBackground(False)
        self.signup_form.setStyleSheet("QGroupBox {\n"
"border: 2px solid gray;\n"
"border-color: #424242;\n"
"border-radius: 15px;\n"
"background-color: white\n"
"}")
        self.signup_form.setTitle("")
        self.signup_form.setObjectName("signup_form")
        self.email_label = QtWidgets.QLabel(self.signup_form)
        self.email_label.setGeometry(QtCore.QRect(20, 10, 211, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.email_entry = QtWidgets.QLineEdit(self.signup_form)
        self.email_entry.setGeometry(QtCore.QRect(20, 70, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.email_entry.setFont(font)
        self.email_entry.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(222, 222, 222);\n"
"    border-radius: 7;\n"
"    border: 1px solid black\n"
"}")
        self.email_entry.setObjectName("email_entry")
        self.password_label = QtWidgets.QLabel(self.signup_form)
        self.password_label.setGeometry(QtCore.QRect(20, 170, 211, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.password_entry = QtWidgets.QLineEdit(self.signup_form)
        self.password_entry.setGeometry(QtCore.QRect(20, 230, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.password_entry.setFont(font)
        self.password_entry.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(222, 222, 222);\n"
"    border-radius: 7;\n"
"    border: 1px solid black\n"
"}")
        self.password_entry.setObjectName("password_entry")
        self.sign_up_button_form = QtWidgets.QPushButton(self.signup_form)
        self.sign_up_button_form.setGeometry(QtCore.QRect(30, 290, 381, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.sign_up_button_form.setFont(font)
        self.sign_up_button_form.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sign_up_button_form.setAutoFillBackground(False)
        self.sign_up_button_form.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0.125, y1:0.466, x2:0.938, y2:0.472, stop:0 rgba(0, 144, 24, 255), stop:1 rgba(124, 255, 38, 255));\n"
"    color: white;\n"
"     border-radius: 10; \n"
"    padding: 6; \n"
"    border-style: outset;\n"
"    border-width: 1;\n"
"    border-top-color: rgb(135, 135, 135);\n"
"    border-left-color: rgb(135, 135, 135);\n"
"    border-right-color: rgb(0, 0, 0);\n"
"    border-bottom-color: rgb(0, 0, 0);\n"
"    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: outset;\n"
"    border-top-color: rgb(0, 0, 0);\n"
"    border-left-color: rgb(0, 0, 0);\n"
"    border-right-color: rgb(135, 135, 135);\n"
"    border-bottom-color: rgb(135, 135, 135);\n"
"    \n"
"}")
        self.sign_up_button_form.setCheckable(False)
        self.sign_up_button_form.setChecked(False)
        self.sign_up_button_form.setDefault(False)
        self.sign_up_button_form.setFlat(False)
        self.sign_up_button_form.setObjectName("sign_up_button_form")
        self.signup_close_button = QtWidgets.QPushButton(self.signup_form)
        self.signup_close_button.setGeometry(QtCore.QRect(400, 10, 41, 41))
        self.signup_close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signup_close_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.signup_close_button.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 6;\n"
"    image: url(:/titleScreen/closebutton.png);\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"\n"
"}")
        self.signup_close_button.setText("")
        self.signup_close_button.setIconSize(QtCore.QSize(40, 40))
        self.signup_close_button.setObjectName("signup_close_button")
        self.signup_failed_format = QtWidgets.QLabel(self.signup_form)
        self.signup_failed_format.setGeometry(QtCore.QRect(30, 260, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signup_failed_format.setFont(font)
        self.signup_failed_format.setStyleSheet("color: red")
        self.signup_failed_format.setAlignment(QtCore.Qt.AlignCenter)
        self.signup_failed_format.setObjectName("signup_failed_format")
        self.signup_failed_in_use = QtWidgets.QLabel(self.signup_form)
        self.signup_failed_in_use.setGeometry(QtCore.QRect(30, 260, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signup_failed_in_use.setFont(font)
        self.signup_failed_in_use.setStyleSheet("color: red")
        self.signup_failed_in_use.setAlignment(QtCore.Qt.AlignCenter)
        self.signup_failed_in_use.setObjectName("signup_failed_in_use")
        self.username_entry = QtWidgets.QLineEdit(self.signup_form)
        self.username_entry.setGeometry(QtCore.QRect(20, 150, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.username_entry.setFont(font)
        self.username_entry.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(222, 222, 222);\n"
"    border-radius: 7;\n"
"    border: 1px solid black\n"
"}")
        self.username_entry.setObjectName("username_entry")
        self.username_label = QtWidgets.QLabel(self.signup_form)
        self.username_label.setGeometry(QtCore.QRect(20, 110, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.signup_failed_password = QtWidgets.QLabel(self.signup_form)
        self.signup_failed_password.setGeometry(QtCore.QRect(30, 260, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signup_failed_password.setFont(font)
        self.signup_failed_password.setStyleSheet("color: red")
        self.signup_failed_password.setAlignment(QtCore.Qt.AlignCenter)
        self.signup_failed_password.setObjectName("signup_failed_password")
        self.signup_failed_username = QtWidgets.QLabel(self.signup_form)
        self.signup_failed_username.setGeometry(QtCore.QRect(30, 260, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signup_failed_username.setFont(font)
        self.signup_failed_username.setStyleSheet("color: red")
        self.signup_failed_username.setAlignment(QtCore.Qt.AlignCenter)
        self.signup_failed_username.setObjectName("signup_failed_username")
        self.sign_up_button = QtWidgets.QPushButton(self.centralwidget)
        self.sign_up_button.setGeometry(QtCore.QRect(340, 440, 381, 81))
        font = QtGui.QFont()
        font.setFamily("Supercell-Magic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.sign_up_button.setFont(font)
        self.sign_up_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sign_up_button.setAutoFillBackground(False)
        self.sign_up_button.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0.125, y1:0.466, x2:0.938, y2:0.472, stop:0 rgba(0, 144, 24, 255), stop:1 rgba(124, 255, 38, 255));\n"
"    color: white;\n"
"     border-radius: 10; \n"
"    padding: 6; \n"
"    border-style: outset;\n"
"    border-width: 1;\n"
"    border-top-color: rgb(135, 135, 135);\n"
"    border-left-color: rgb(135, 135, 135);\n"
"    border-right-color: rgb(0, 0, 0);\n"
"    border-bottom-color: rgb(0, 0, 0);\n"
"    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: outset;\n"
"    border-top-color: rgb(0, 0, 0);\n"
"    border-left-color: rgb(0, 0, 0);\n"
"    border-right-color: rgb(135, 135, 135);\n"
"    border-bottom-color: rgb(135, 135, 135);\n"
"    \n"
"}")
        self.sign_up_button.setCheckable(False)
        self.sign_up_button.setChecked(False)
        self.sign_up_button.setDefault(False)
        self.sign_up_button.setFlat(False)
        self.sign_up_button.setObjectName("sign_up_button")
        self.title_image.raise_()
        self.log_in_button.raise_()
        self.sign_up_button.raise_()
        self.signup_form.raise_()
        self.login_form.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clash Clan Manager"))
        self.email_label_login.setText(_translate("MainWindow", "Email"))
        self.email_entry_login.setPlaceholderText(_translate("MainWindow", "Enter email..."))
        self.password_label_login.setText(_translate("MainWindow", "Password"))
        self.password_entry_login.setPlaceholderText(_translate("MainWindow", "Enter password..."))
        self.log_in_button_login.setText(_translate("MainWindow", "LOG IN"))
        self.login_failed.setText(_translate("MainWindow", "Login failed! Please check your details are correct and try again."))
        self.log_in_button.setText(_translate("MainWindow", "LOG IN"))
        self.email_label.setText(_translate("MainWindow", "Email"))
        self.email_entry.setPlaceholderText(_translate("MainWindow", "Enter email..."))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.password_entry.setPlaceholderText(_translate("MainWindow", "Enter password..."))
        self.sign_up_button_form.setText(_translate("MainWindow", "SIGN UP"))
        self.signup_failed_format.setText(_translate("MainWindow", "Email format is incorrect!"))
        self.signup_failed_in_use.setText(_translate("MainWindow", "Email is already in use! Please try logging in."))
        self.username_entry.setPlaceholderText(_translate("MainWindow", "Enter username..."))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.signup_failed_password.setText(_translate("MainWindow", "Password must be more than 6 characters!"))
        self.signup_failed_username.setText(_translate("MainWindow", "Username must be less than 16 characters!"))
        self.sign_up_button.setText(_translate("MainWindow", "SIGN UP"))
import source


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
