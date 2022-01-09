import io
import PIL
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick
from PyQt5.uic import loadUi
import sys
import os
from pyasn1.type import tag
from pyasn1.type.char import PrintableString
from pyasn1_modules.rfc2459 import PostOfficeBoxAddress
import requests
import pyrebase
import threading
import time
from datetime import datetime, timedelta, timezone, tzinfo
import pytz
from dateutil import parser
import concurrent.futures

from PIL import *
from PIL.ImageQt import ImageQt, QPixmap
from PyQt5.uic.uiparser import WidgetStack
from requests.api import delete
from requests.models import Response

from ui_main import Ui_MainWindow
from add_clan import Ui_addClan
from selection_function import Ui_selectionFunction
from members import Ui_members
from war_cwl import Ui_cwl_war
from headers import headers, firebase_config

username = ''
email = ''
clan_name = ''
loop_closed = False

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

class TitleScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.intro_animation()

        #signup select
        self.ui.sign_up_button.clicked.connect(self.show_signup_form)

        #actually signing up
        self.ui.sign_up_button_form.clicked.connect(self.signup_user)

        #login select
        self.ui.log_in_button.clicked.connect(self.show_login_form)

        #actually logging in
        self.ui.log_in_button_login.clicked.connect(self.login_verification)

        #close login form
        self.ui.login_close_button.clicked.connect(self.hide_login_form)

        #close signup form
        self.ui.signup_close_button.clicked.connect(self.hide_signup_form)

        #adding event shit
        self.ui.log_in_button.installEventFilter(self)
        self.ui.sign_up_button.installEventFilter(self)
        self.ui.log_in_button_login.installEventFilter(self)
        self.ui.sign_up_button_form.installEventFilter(self)

        #hiding passwords
        self.ui.password_entry_login.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.signup_form.hide()
        self.ui.login_form.hide()
        self.ui.login_failed.hide()
        self.ui.signup_failed_format.hide()
        self.ui.signup_failed_in_use.hide()
        self.ui.signup_failed_password.hide()
        self.ui.signup_failed_username.hide()

    def login_verification(self):
        global username
        global email

        email = self.ui.email_entry_login.text()
        password = self.ui.password_entry_login.text()

        try:
            auth.sign_in_with_email_and_password(email, password)
            username = db.child('accounts').child(email.replace('.', '')).get().val()['username']

            stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
            screen2.set_logout_name()
            screen2.load_clans()

            self.ui.email_entry_login.setText('')
            self.ui.password_entry_login.setText('')

            self.ui.login_form.hide()
        except:
            self.ui.login_failed.show()

    def show_signup_form(self):
        self.ui.signup_form.show()

    def hide_signup_form(self):
        self.ui.signup_form.hide()
        
    def show_login_form(self):
        self.ui.login_form.show()

    def hide_login_form(self):
        self.ui.login_form.hide()

    def intro_animation(self):

        #setting opacity effect

        #title
        title_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.title_image)
        self.ui.title_image.setGraphicsEffect(title_opacity_effect)

        #login button
        login_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.log_in_button)
        self.ui.log_in_button.setGraphicsEffect(login_opacity_effect)

        #signup button
        signup_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.sign_up_button)
        self.ui.sign_up_button.setGraphicsEffect(signup_opacity_effect)

        #title animations
        title_geometry_animation = QtCore.QPropertyAnimation(self.ui.title_image, b'geometry', duration=1000, startValue=QtCore.QRect(190, -60, 671, 261), endValue=QtCore.QRect(190, 0, 671, 261))
        title_opacity_animation = QtCore.QPropertyAnimation(title_opacity_effect, b'opacity', duration=1000, startValue=0, endValue=1)

        #button animations
        login_opacity_animation = QtCore.QPropertyAnimation(login_opacity_effect, b'opacity', duration=1000, startValue=0, endValue=1)
        signup_opacity_animation = QtCore.QPropertyAnimation(signup_opacity_effect, b'opacity', duration=1000, startValue=0, endValue=1)

        group = QtCore.QParallelAnimationGroup(self.ui.title_image)
        group.addAnimation(title_geometry_animation)
        group.addAnimation(title_opacity_animation)
        group.addAnimation(login_opacity_animation)
        group.addAnimation(signup_opacity_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def signup_user(self):
        email = self.ui.email_entry.text()
        username = self.ui.username_entry.text()
        password = self.ui.password_entry.text()

        if '@' and '.' in email:
            if len(username) <= 16:
                if len(password) >= 6:
                    try:
                        auth.create_user_with_email_and_password(email, password)

                        data = {'username': username}
                        db.child('accounts').child(email.replace('.', '')).set(data)

                        self.ui.username_entry.setText('')
                        self.ui.password_entry.setText('')

                        self.ui.signup_form.hide()
                    except:
                        self.ui.signup_failed_in_use.show()
                else:
                    self.ui.signup_failed_password.show()
            else:
                self.ui.signup_failed_username.show()
        else:
            self.ui.signup_failed_format.show()

class AddClanScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_addClan()
        self.ui.setupUi(self)

        #add clan
        self.ui.add_clan_button.clicked.connect(self.animate_add_clan_box)

        #retrieve clan
        self.ui.search_clan_button.clicked.connect(self.retrieve_clan)

        #confirm clan
        self.ui.confirm_clan.clicked.connect(self.confirm_clan)

        #hide da bins
        self.ui.delete_0.hide()
        self.ui.delete_1.hide()
        self.ui.delete_2.hide()
        self.ui.delete_3.hide()
        self.ui.delete_4.hide()

        #hide the confirmy things
        self.ui.confirm_0.hide()
        self.ui.confirm_1.hide()
        self.ui.confirm_2.hide()
        self.ui.confirm_3.hide()
        self.ui.confirm_4.hide()

        #make bins do things
        self.ui.delete_0.clicked.connect(lambda: self.remove_clans(0))
        self.ui.delete_1.clicked.connect(lambda: self.remove_clans(1))
        self.ui.delete_2.clicked.connect(lambda: self.remove_clans(2))
        self.ui.delete_3.clicked.connect(lambda: self.remove_clans(3))
        self.ui.delete_4.clicked.connect(lambda: self.remove_clans(4))

        #select clan
        self.ui.confirm_0.clicked.connect(lambda: self.select_clan(0))
        self.ui.confirm_1.clicked.connect(lambda: self.select_clan(1))
        self.ui.confirm_2.clicked.connect(lambda: self.select_clan(2))
        self.ui.confirm_3.clicked.connect(lambda: self.select_clan(3))
        self.ui.confirm_4.clicked.connect(lambda: self.select_clan(4))

        #logout
        self.ui.logout_button.clicked.connect(self.logout)

        #adding event filter
        self.ui.clan_shield_0.installEventFilter(self)
        self.ui.clan_name_0.installEventFilter(self)
        self.ui.delete_0.installEventFilter(self)
        self.ui.confirm_0.installEventFilter(self)

        self.ui.clan_shield_1.installEventFilter(self)
        self.ui.clan_name_1.installEventFilter(self)
        self.ui.delete_1.installEventFilter(self)
        self.ui.confirm_1.installEventFilter(self)

        self.ui.clan_shield_2.installEventFilter(self)
        self.ui.clan_name_2.installEventFilter(self)
        self.ui.delete_2.installEventFilter(self)
        self.ui.confirm_2.installEventFilter(self)

        self.ui.clan_shield_3.installEventFilter(self)
        self.ui.clan_name_3.installEventFilter(self)
        self.ui.delete_3.installEventFilter(self)
        self.ui.confirm_3.installEventFilter(self)

        self.ui.clan_shield_4.installEventFilter(self)
        self.ui.clan_name_4.installEventFilter(self)
        self.ui.delete_4.installEventFilter(self)
        self.ui.confirm_4.installEventFilter(self)

        #make add clan go poof
        self.ui.add_clan_close_button.clicked.connect(self.animate_add_clan_box_remove)

        self.ui.add_clan_group.hide()
        self.ui.clan_description.hide()
        self.ui.no_clan.hide()

    def select_clan(self, clan_number):
        global clan_name

        clan_name = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan' + str(clan_number)).child('tag').get().val()
        screen3.set_clan()

        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)

        screen3.set_logout_name()

    def set_logout_name(self):
        self.ui.logout_button.setText('Log Out: ' + username)

    def eventFilter(self,object,event):
        if event.type() == QtCore.QEvent.Enter:
            if object == self.ui.clan_shield_0 or object == self.ui.clan_name_0 or object == self.ui.delete_0 or object == self.ui.confirm_0:
                self.ui.frame_0.setStyleSheet('background-color: rgb(227, 227, 227);')
            elif object == self.ui.clan_shield_1 or object == self.ui.clan_name_1 or object == self.ui.delete_1 or object == self.ui.confirm_1:
                self.ui.frame_1.setStyleSheet('background-color: rgb(227, 227, 227);')
            elif object == self.ui.clan_shield_2 or object == self.ui.clan_name_2 or object == self.ui.delete_2 or object == self.ui.confirm_2:
                self.ui.frame_2.setStyleSheet('background-color: rgb(227, 227, 227);')
            elif object == self.ui.clan_shield_3 or object == self.ui.clan_name_3 or object == self.ui.delete_3 or object == self.ui.confirm_3:
                self.ui.frame_3.setStyleSheet('background-color: rgb(227, 227, 227);')
            elif object == self.ui.clan_shield_4 or object == self.ui.clan_name_4 or object == self.ui.delete_4 or object == self.ui.confirm_4:
                self.ui.frame_4.setStyleSheet('background-color: rgb(227, 227, 227);')
            return True
        elif event.type() == QtCore.QEvent.Leave:
            if object == self.ui.clan_shield_0 or object == self.ui.clan_name_0 or object == self.ui.delete_0 or object == self.ui.confirm_0:
                self.ui.frame_0.setStyleSheet('QFrame {\n'
    'background-color: white;\n'
    '}\n'
    '\n'
    'QFrame:hover {\n'
    'background-color: rgb(227, 227, 227);\n'
    '}')
            elif object == self.ui.clan_shield_1 or object == self.ui.clan_name_1 or object == self.ui.delete_1 or object == self.ui.confirm_1:
                self.ui.frame_1.setStyleSheet('QFrame {\n'
    'background-color: white;\n'
    '}\n'
    '\n'
    'QFrame:hover {\n'
    'background-color: rgb(227, 227, 227);\n'
    '}')
            elif object == self.ui.clan_shield_2 or object == self.ui.clan_name_2 or object == self.ui.delete_2 or object == self.ui.confirm_2:
                self.ui.frame_2.setStyleSheet('QFrame {\n'
    'background-color: white;\n'
    '}\n'
    '\n'
    'QFrame:hover {\n'
    'background-color: rgb(227, 227, 227);\n'
    '}')
            elif object == self.ui.clan_shield_3 or object == self.ui.clan_name_3 or object == self.ui.delete_3 or object == self.ui.confirm_3:
                self.ui.frame_3.setStyleSheet('QFrame {\n'
    'background-color: white;\n'
    '}\n'
    '\n'
    'QFrame:hover {\n'
    'background-color: rgb(227, 227, 227);\n'
    '}')
            elif object == self.ui.clan_shield_4 or object == self.ui.clan_name_4 or object == self.ui.delete_4 or object == self.ui.confirm_4:
                self.ui.frame_4.setStyleSheet('QFrame {\n'
    'background-color: white;\n'
    '}\n'
    '\n'
    'QFrame:hover {\n'
    'background-color: rgb(227, 227, 227);\n'
    '}')
            return True
        else:
            return False

    def load_clans(self):

        def load_clan_0():
            try:
                clan_0 = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan0').child('tag').get().val()

                clan_0_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_0, headers = headers)
                if clan_0_response.status_code == 200:
                    clan_0_json = clan_0_response.json()

                    self.ui.clan_name_0.setText(clan_0_json['name'])
                    self.ui.delete_0.show()
                    self.ui.confirm_0.show()

                    image_0_response = requests.get(clan_0_json['badgeUrls']['large'])

                if image_0_response.status_code == 200:
                    image_bytes = io.BytesIO(image_0_response.content)
                    img = Image.open(image_bytes)
                    qimage = ImageQt(img)

                    self.ui.clan_shield_0.setPixmap(QtGui.QPixmap.fromImage(qimage))
                else:
                    pass
            except:
                self.ui.clan_name_0.setText('')
                self.ui.clan_shield_0.setPixmap(QtGui.QPixmap())
                self.ui.delete_0.hide()
                self.ui.confirm_0.hide()

        def load_clan_1():
            try:
                clan_1 = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan1').child('tag').get().val()

                clan_1_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_1, headers = headers)
                if clan_1_response.status_code == 200:
                    clan_1_json = clan_1_response.json()

                    self.ui.clan_name_1.setText(clan_1_json['name'])
                    self.ui.delete_1.show()
                    self.ui.confirm_1.show()

                    image_1_response = requests.get(clan_1_json['badgeUrls']['large'])

                if image_1_response.status_code == 200:
                    image_bytes = io.BytesIO(image_1_response.content)
                    img = Image.open(image_bytes)
                    qimage = ImageQt(img)

                    self.ui.clan_shield_1.setPixmap(QtGui.QPixmap.fromImage(qimage))
                else:
                    pass
            except:
                self.ui.clan_name_1.setText('')
                self.ui.clan_shield_1.setPixmap(QtGui.QPixmap())
                self.ui.delete_1.hide()
                self.ui.confirm_1.hide()

        def load_clan_2():
            try:
                clan_2 = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan2').child('tag').get().val()

                clan_2_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_2, headers = headers)
                if clan_2_response.status_code == 200:
                    clan_2_json = clan_2_response.json()

                    self.ui.clan_name_2.setText(clan_2_json['name'])
                    self.ui.delete_2.show()
                    self.ui.confirm_2.show()

                    image_2_response = requests.get(clan_2_json['badgeUrls']['large'])

                if image_2_response.status_code == 200:
                    image_bytes = io.BytesIO(image_2_response.content)
                    img = Image.open(image_bytes)
                    qimage = ImageQt(img)

                    self.ui.clan_shield_2.setPixmap(QtGui.QPixmap.fromImage(qimage))
                else:
                    pass
            except:
                self.ui.clan_name_2.setText('')
                self.ui.clan_shield_2.setPixmap(QtGui.QPixmap())
                self.ui.delete_2.hide()
                self.ui.confirm_2.hide()

        def load_clan_3():
            try:
                clan_3 = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan3').child('tag').get().val()

                clan_3_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_3, headers = headers)
                if clan_3_response.status_code == 200:
                    clan_3_json = clan_3_response.json()

                    self.ui.clan_name_3.setText(clan_3_json['name'])
                    self.ui.delete_3.show()
                    self.ui.confirm_3.show()

                    image_3_response = requests.get(clan_3_json['badgeUrls']['large'])

                if image_3_response.status_code == 200:
                    image_bytes = io.BytesIO(image_3_response.content)
                    img = Image.open(image_bytes)
                    qimage = ImageQt(img)

                    self.ui.clan_shield_3.setPixmap(QtGui.QPixmap.fromImage(qimage))
                else:
                    pass
            except:
                self.ui.clan_name_3.setText('')
                self.ui.clan_shield_3.setPixmap(QtGui.QPixmap())
                self.ui.delete_3.hide()
                self.ui.confirm_3.hide()

        def load_clan_4():
            try:
                clan_4 = db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan4').child('tag').get().val()

                clan_4_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_4, headers = headers)
                if clan_4_response.status_code == 200:
                    clan_4_json = clan_4_response.json()

                    self.ui.clan_name_4.setText(clan_4_json['name'])
                    self.ui.delete_4.show()
                    self.ui.confirm_4.show()

                    image_4_response = requests.get(clan_4_json['badgeUrls']['large'])

                if image_4_response.status_code == 200:
                    image_bytes = io.BytesIO(image_4_response.content)
                    img = Image.open(image_bytes)
                    qimage = ImageQt(img)

                    self.ui.clan_shield_4.setPixmap(QtGui.QPixmap.fromImage(qimage))
                else:
                    pass
            except:
                self.ui.clan_name_4.setText('')
                self.ui.clan_shield_4.setPixmap(QtGui.QPixmap())
                self.ui.delete_4.hide()
                self.ui.confirm_4.hide()

        t1 = threading.Thread(target=load_clan_0)
        t2 = threading.Thread(target=load_clan_1)
        t3 = threading.Thread(target=load_clan_2)
        t4 = threading.Thread(target=load_clan_3)
        t5 = threading.Thread(target=load_clan_4)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

    def remove_clans(self, line_number):

        db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan' + str(line_number)).remove()

        clans_left = []

        try:
            clans_left.append(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()['savedclan0'])
        except:
            pass
        try:
            clans_left.append(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()['savedclan1'])
        except:
            pass
        try:
            clans_left.append(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()['savedclan2'])
        except:
            pass
        try:
            clans_left.append(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()['savedclan3'])
        except:
            pass
        try:
            clans_left.append(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()['savedclan4'])
        except:
            pass

        count = 0

        for _ in range(5):
            try:
                current_clan = 'savedclan' + str(count)
                data = {current_clan: clans_left[count]}
                db.child('accounts').child(email.replace('.', '')).child('saved clans').update(data)
            except:
                db.child('accounts').child(email.replace('.', '')).child('saved clans').child(current_clan).remove()

            count = count + 1

        self.load_clans()

    def logout(self):
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex()-1)

    def animate_clan_list_screen(self):
        #background
        window_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.background_image)
        self.ui.background_image.setGraphicsEffect(window_opacity_effect)

        #list
        list_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.clans_list)
        self.ui.clans_list.setGraphicsEffect(list_opacity_effect)

        #button
        new_clan_opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.add_clan_button)
        self.ui.add_clan_button.setGraphicsEffect(new_clan_opacity_effect)

        #animations
        window_opacity_animation = QtCore.QPropertyAnimation(window_opacity_effect, b'opacity', duration=10000, startValue=0, endValue=1)
        list_opacity_animation = QtCore.QPropertyAnimation(list_opacity_effect, b'opacity', duration=10000, startValue=0, endValue=1)
        new_clan_opacity_animation = QtCore.QPropertyAnimation(new_clan_opacity_effect, b'opacity', duration=10000, startValue=0, endValue=1)

        list_group = QtCore.QParallelAnimationGroup(self.ui.background_image)
        list_group.addAnimation(window_opacity_animation)
        list_group.addAnimation(list_opacity_animation)
        list_group.addAnimation(new_clan_opacity_animation)
        list_group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def animate_add_clan_box(self):
        self.ui.add_clan_group.show()

        add_clan_box_animation = QtCore.QPropertyAnimation(self.ui.add_clan_group, b'geometry', duration=200, startValue=QtCore.QRect(220, -300, 631, 301), endValue=QtCore.QRect(220, 150, 631, 301))

        group = QtCore.QParallelAnimationGroup(self.ui.add_clan_group)
        group.addAnimation(add_clan_box_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def retrieve_clan(self):
        clan_tag = self.ui.clan_entry.text().lstrip('#')

        response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_tag, headers = headers)
        if response.status_code == 200:
            self.ui.no_clan.hide()
            clan_json = response.json()

            self.ui.clan_name.setText(clan_json['name'])
            self.ui.clan_description.setText(clan_json['description'])

            image_response = requests.get(clan_json['badgeUrls']['large'])

            if image_response.status_code == 200:
                image_bytes = io.BytesIO(image_response.content)
                img = Image.open(image_bytes)
                qimage = ImageQt(img)

                self.ui.clan_shield.setPixmap(QtGui.QPixmap.fromImage(qimage))
                self.ui.clan_description.show()
        else:
            self.ui.no_clan.show()

    def animate_add_clan_box_remove(self):
        add_clan_box_animation = QtCore.QPropertyAnimation(self.ui.add_clan_group, b'geometry', duration=200, startValue=QtCore.QRect(220, 150, 631, 301), endValue=QtCore.QRect(220, -300, 631, 301))

        group = QtCore.QParallelAnimationGroup(self.ui.add_clan_group)
        group.addAnimation(add_clan_box_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def confirm_clan(self):
        add_clan_box_animation = QtCore.QPropertyAnimation(self.ui.add_clan_group, b'geometry', duration=200, startValue=QtCore.QRect(220, 150, 631, 301), endValue=QtCore.QRect(220, -300, 631, 301))

        group = QtCore.QParallelAnimationGroup(self.ui.add_clan_group)
        group.addAnimation(add_clan_box_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        clan_tag = self.ui.clan_entry.text().lstrip('#')

        try:
            if len(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val()) < 5:

                def repeat_local_clan():
                    for i in range(len(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val())):
                        if db.child('accounts').child(email.replace('.', '')).child('saved clans').child('savedclan' + str(i)).child('tag').get().val() == clan_tag:
                            return True
                    return False

                if repeat_local_clan() == False:
                    clan_number = len(db.child('accounts').child(email.replace('.', '')).child('saved clans').get().val())
                    clan_name = 'savedclan' + str(clan_number)

                    data = {'tag': clan_tag}

                    db.child('accounts').child(email.replace('.', '')).child('saved clans').child(clan_name).set(data)
        except:
            clan_name = 'savedclan0'

            data = {'tag': clan_tag}

            db.child('accounts').child(email.replace('.', '')).child('saved clans').child(clan_name).set(data)
        
        try:
            clan_number = len(db.child('clans').get().val())
        except:
            clan_number = 0

        def repeat_global_clan():
            for i in range(clan_number):
                if db.child('clans').child(str(i)).child('tag').get().val() == clan_tag:
                    return True
            return False
        
        if repeat_global_clan() == False:
            db.child('clans').child(clan_number).set({'tag': clan_tag})

        self.load_clans()
        self.ui.clan_entry.setText('#')
        self.ui.clan_description.hide()
        self.ui.clan_shield.setPixmap(QtGui.QPixmap())
        self.ui.clan_name.setText('')

class selectionFunctionScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_selectionFunction()
        self.ui.setupUi(self)

        #logout
        self.ui.logout_button.clicked.connect(self.logout)\

        #hide the filler thing
        self.ui.filler_label.hide()

        #change clan
        self.ui.change_clan_button.clicked.connect(self.change_clan)

        #go to war
        self.ui.war_button.clicked.connect(self.war)

        #hide progresbar text
        self.ui.progressBar.setTextVisible(False)

        #clan name dropshadow
        dropshadow_effect = QtWidgets.QGraphicsDropShadowEffect(self.ui.clan_name)
        dropshadow_effect.setOffset(0,0)
        dropshadow_effect.setBlurRadius(50)
        dropshadow_effect.setColor(QtGui.QColor(0,0,0,255))
        self.ui.clan_name.setGraphicsEffect(dropshadow_effect)

        #members list
        self.ui.members_button.clicked.connect(self.members)

        #hide progress bar
        self.ui.progressBar.hide()

    def members(self):
        screen4.load_clan()
        screen4.set_logout_name()

    def set_logout_name(self):
        self.ui.logout_button.setText('Log Out: ' + username)

    def logout(self):
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex()-2)

    def change_clan(self):
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() - 1)

    def war(self):
        stacked_widget.setCurrentIndex(4)
        screen5.set_logout_name()
        screen5.load_clan()

    def set_clan(self):
        response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_name, headers = headers)
        if response.status_code == 200:
            response_json = response.json()

            self.ui.clan_name.setText(response_json['name'])
            image_response = requests.get(response_json['badgeUrls']['large'])

            if image_response.status_code == 200:
                image_bytes = io.BytesIO(image_response.content)
                img = Image.open(image_bytes)
                qimage = ImageQt(img)

                self.ui.clan_shield.setPixmap(QtGui.QPixmap.fromImage(qimage))

class membersScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_members()
        self.ui.setupUi(self)

        #logout
        self.ui.logout_button.clicked.connect(self.logout)

        #go back
        self.ui.back_button.clicked.connect(self.back)

    def load_clan(self):
        name_response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_name, headers = headers)
        if name_response.status_code == 200:
            name_response_json = name_response.json()

            self.ui.clan_name.setText(name_response_json['name'])
            member_count = name_response_json['members']
            self.ui.member_count.setText(str(member_count) + '/50')

            image_0_response = requests.get(name_response_json['badgeUrls']['large'])

            loop_number = 50 - name_response_json['members']

            for x in range(50):
                self.ui.scrollAreaWidgetContents.children()[x+1].show()

            for i in range(loop_number):
                self.ui.scrollAreaWidgetContents.children()[i+1].hide()
            
            screen3.ui.filler_label.show()

            def members(index):
                try:
                    profile_response = requests.get('https://cocproxy.royaleapi.dev/v1/players/%23' + name_response_json['memberList'][index]['tag'].lstrip('#'), headers = headers)
                    if profile_response.status_code == 200:
                        profile_response_json = profile_response.json()

                    #set name
                    name = name_response_json['memberList'][index]['name']
                    #set xp
                    xp = name_response_json['memberList'][index]['expLevel']
                    #set town hall
                    town_hall_level = profile_response_json['townHallLevel']
                    #set trophy badge and amount
                    trophies = profile_response_json['trophies']
                    #set war stars amount
                    war_stars = profile_response_json['warStars']
                    #set donations given amount
                    donations = profile_response_json['donations']
                    #set donations received amount
                    donations_received = profile_response_json['donationsReceived']
                    try:
                        donation_ratio = round(profile_response_json['donations'] / profile_response_json['donationsReceived'], 2)
                    except:
                        donation_ratio = donations
                    #set hero levels amount
                    hero_levels = []
                    try:
                        if profile_response_json['heroes'][0]['name'] != 'Battle Machine':
                            bk_level = profile_response_json['heroes'][0]['level']
                            hero_levels.append(bk_level)
                    except:
                        pass
                    try:
                        if profile_response_json['heroes'][1]['name'] != 'Battle Machine':
                            aq_level = profile_response_json['heroes'][1]['level']
                            hero_levels.append(aq_level)
                    except:
                        pass
                    try:
                        if profile_response_json['heroes'][2]['name'] != 'Battle Machine':
                            gw_level = profile_response_json['heroes'][2]['level']
                            hero_levels.append(gw_level)
                    except:
                        pass
                    try:
                        if profile_response_json['heroes'][3]['name'] != 'Battle Machine':
                            rc_level = profile_response_json['heroes'][3]['level']
                            hero_levels.append(rc_level)
                    except:
                        pass
                    try:
                        if profile_response_json['heroes'][4]['name'] != 'Battle Machine':
                            rc_level = profile_response_json['heroes'][4]['level']
                            hero_levels.append(rc_level)
                    except:
                        pass
                    try:
                        average_hero_level = round(sum(hero_levels) / len(hero_levels), 1)
                    except:
                        average_hero_level = '0.0'

                    war_preference = profile_response_json['warPreference']

                    return {'name': name, 'xp': xp, 'town_hall_level': town_hall_level, 'trophies': trophies, 'war_stars': war_stars, 'donations': donations, 'donations_received': donations_received,
                            'donation_ratio': float(donation_ratio), 'average_hero_level': float(average_hero_level), 'war_preference': war_preference}
                except:
                    pass
                
            members_list_threads = []
            members_list = []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(name_response_json['members']):
                    members_list_threads.append(executor.submit(members, i))
            
            for i in range(name_response_json['members']):
                members_list.append(members_list_threads[i].result())

        if image_0_response.status_code == 200:
            image_bytes = io.BytesIO(image_0_response.content)
            img = Image.open(image_bytes)
            qimage = ImageQt(img)

            self.ui.clan_image.setPixmap(QtGui.QPixmap.fromImage(qimage))
        else:
            pass

        self.ui.town_hall_button.clicked.connect(lambda: self.sort(member_count, members_list, 'town_hall_level'))
        self.ui.trophy_button.clicked.connect(lambda: self.sort(member_count, members_list, 'trophies'))
        self.ui.war_stars_button.clicked.connect(lambda: self.sort(member_count, members_list, 'war_stars'))
        self.ui.donations_given_button.clicked.connect(lambda: self.sort(member_count, members_list, 'donations'))
        self.ui.donations_received_button.clicked.connect(lambda: self.sort(member_count, members_list, 'donations_received'))
        self.ui.donation_ratio_button.clicked.connect(lambda: self.sort(member_count, members_list, 'donation_ratio'))
        self.ui.average_hero_button.clicked.connect(lambda: self.sort(member_count, members_list, 'average_hero_level'))

        self.show_members(member_count, members_list)

        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
        screen3.ui.filler_label.hide()
    
    def show_members(self, member_count, members_list):
        for i in range(member_count):
            index = 50 - i

            self.ui.scrollAreaWidgetContents.children()[index].children()[3].setText(members_list[i]['name'])
            self.ui.scrollAreaWidgetContents.children()[index].children()[4].setText(str(members_list[i]['xp']))
            self.ui.scrollAreaWidgetContents.children()[index].children()[1].setStyleSheet('border-image: url(:/members/townhall' + str(members_list[i]['town_hall_level']) + '.png);')
            self.ui.scrollAreaWidgetContents.children()[index].children()[6].setText(str(members_list[i]['trophies']))
            if members_list[i]['trophies'] <= 399:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/unranked.png);')
            elif 399 <= members_list[i]['trophies'] <= 799:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/bronze.png);')
            elif 799 <= members_list[i]['trophies'] <= 1399:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/silver.png);')
            elif 1399 <= members_list[i]['trophies'] <= 1999:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/gold.png);')
            elif 1999 <= members_list[i]['trophies'] <= 2599:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/crystal.png);')
            elif 2599 <= members_list[i]['trophies'] <= 3199:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/master.png);')
            elif 3199 <= members_list[i]['trophies'] <= 4099:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/champion.png);')
            elif 4099 <= members_list[i]['trophies'] <= 4999:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/titan.png);')
            elif members_list[i]['trophies'] >= 5000:
                self.ui.scrollAreaWidgetContents.children()[index].children()[5].setStyleSheet('border-image: url(:/members/legend.png);')
            self.ui.scrollAreaWidgetContents.children()[index].children()[8].setText(str(members_list[i]['war_stars']))
            self.ui.scrollAreaWidgetContents.children()[index].children()[10].setText(str(members_list[i]['donations']))
            self.ui.scrollAreaWidgetContents.children()[index].children()[11].setText(str(members_list[i]['donations_received']))
            self.ui.scrollAreaWidgetContents.children()[index].children()[12].setText(str(members_list[i]['donation_ratio']))
            self.ui.scrollAreaWidgetContents.children()[index].children()[14].setText(str(members_list[i]['average_hero_level']))
            if members_list[i]['war_preference'] == 'in':
                self.ui.scrollAreaWidgetContents.children()[index].children()[15].setStyleSheet('border-image: url(:/members/greenwarshield.png);')
            elif members_list[i]['war_preference'] == 'out':
                self.ui.scrollAreaWidgetContents.children()[index].children()[15].setStyleSheet('border-image: url(:/members/redwarshield.png);')

    def sort(self, member_count, members_list, key):
        new_members_list = sorted(members_list, key=lambda d: d[key], reverse=True)
        
        if new_members_list == members_list:
            members_list.sort(key=lambda d: d[key])
        else:
            members_list.sort(key=lambda d: d[key], reverse=True)

        self.show_members(member_count, members_list)

    def set_logout_name(self):
        self.ui.logout_button.setText('Log Out: ' + username)

    def logout(self):
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex()-3)

    def back(self):
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex()-1)

class warCwlScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_cwl_war()
        self.ui.setupUi(self)

        self.ui.details_header.hide()
        self.ui.current_war_more_details_box.hide()
        self.ui.participant_information_box.hide()

        #logout
        self.ui.logout_button.clicked.connect(self.logout)

        #back
        self.ui.back_button.clicked.connect(self.back)

        #show details box
        self.ui.current_war_more_details_button.clicked.connect(self.show_more_details)

        #hide stuff
        self.ui.login_close_button.clicked.connect(self.close_show_more_details)
        self.ui.participant_information_box_close_button.clicked.connect(self.close_participant_information_box)

        #set opacity
        details_clan_image_1_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.details_clan_image_1)
        details_clan_image_1_effect.setOpacity(0.2)
        self.ui.details_clan_image_1.setGraphicsEffect(details_clan_image_1_effect)

        details_clan_image_2_effect = QtWidgets.QGraphicsOpacityEffect(self.ui.details_clan_image_2)
        details_clan_image_2_effect.setOpacity(0.2)
        self.ui.details_clan_image_2.setGraphicsEffect(details_clan_image_2_effect)

    def logout(self):
        stacked_widget.setCurrentIndex(0)

    def back(self):
        stacked_widget.setCurrentIndex(2)

    def set_logout_name(self):
        self.ui.logout_button.setText('Log Out: ' + username)

    def show_more_details(self):
        self.ui.details_header.show()
        self.ui.current_war_more_details_box.show()

    def close_show_more_details(self):
        self.ui.details_header.hide()
        self.ui.current_war_more_details_box.hide()
        self.ui.participant_information_box.hide()

    def close_participant_information_box(self):
        self.ui.participant_information_box.hide()

    def load_clan(self):
        self.ui.details_header.hide()
        self.ui.current_war_more_details_box.hide()

        for i in range (len(self.ui.current_war_box.children())):
            self.ui.current_war_box.children()[i].show()

        self.ui.no_war_found.hide()

        try:
            response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_name + '/currentwar', headers = headers)
            if response.status_code == 200:
                response_json = response.json()

                friendly_participants = response_json['clan']['members']
                enemy_participants = response_json['opponent']['members']
                participants = {'clan': friendly_participants, 'opponent': enemy_participants}

                self.display_information(response_json, 'clan', 'opponent')
                self.load_war_participants(response_json, 'clan', 'opponent', participants)

            elif response.status_code == 403:
                for i in self.ui.current_war_box.children():
                    i.hide()

                self.ui.no_war_found.setText('Public War Log Disabled')
                self.ui.current_war_label.show()
                self.ui.no_war_found.show()
        except:
            response = requests.get('https://cocproxy.royaleapi.dev/v1/clans/%23' + clan_name + '/currentwar/leaguegroup', headers = headers)
            if response.status_code == 200:
                response_json = response.json()

                def war_search(index):

                    def individual_war_search(war_index):
                        war_response = requests.get('https://cocproxy.royaleapi.dev/v1/clanwarleagues/wars/%23' + response_json['rounds'][index]['warTags'][war_index].lstrip('#'), headers = headers)
                        if war_response.status_code == 200:
                            war_response_json = war_response.json()

                            try:
                                if war_response_json['state'] == 'inWar' or (index == 0 and war_response_json['state'] == 'preparation'):
                                    if war_response_json['clan']['tag'].lstrip('#') == clan_name:
                                        clan_status = 'clan'
                                        opponent_status = 'opponent'
                                        return war_response_json, clan_status, opponent_status
                                    elif war_response_json['opponent']['tag'].lstrip('#') == clan_name:
                                        clan_status = 'opponent'
                                        opponent_status = 'clan'
                                        return war_response_json, clan_status, opponent_status
                            except:
                                return None
                        else:
                            return None
                    
                    threads = []

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        for i in range(4):
                            threads.append(executor.submit(individual_war_search, i))

                    for i in range(len(threads)):
                        if threads[i].result() != None:
                            return threads[i].result()
                
                threads = []

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    for i in range(7):
                        threads.append(executor.submit(war_search, i))
                
                threads_results = []
                
                for i in range(7):
                    threads_results.append(threads[i].result())
                    if threads_results[i] != None:
                        response_json, clan_status, opponent_status = threads_results[i][0], threads_results[i][1], threads_results[i][2]

                friendly_participants = response_json[clan_status]['members']
                enemy_participants = response_json[opponent_status]['members']

                participants = {'clan': friendly_participants, 'opponent': enemy_participants}

                self.display_information(response_json, clan_status, opponent_status)
                self.load_war_participants(response_json, clan_status, opponent_status, participants)

            else:
                for i in range(len(self.ui.current_war_box.children())):
                    self.ui.current_war_box.children()[i].hide()

                self.ui.no_war_found.setText('No Recent War Found')
                self.ui.current_war_label.show()
                self.ui.no_war_found.show()
        
    def display_information(self, response_json, clan_status, opponent_status):
        team_size = response_json['teamSize']

        if response_json['state'] == 'inWar':
            current_time = datetime.now(tz=timezone.utc)

            war_end = response_json['endTime']
            war_end_parsed = parser.parse(war_end)

            time_left = war_end_parsed - current_time

            self.ui.war_prep_end_label.setText('War End')
        elif response_json['state'] == 'warEnded':

            self.ui.war_prep_end_label.setText('War Ended')
            self.ui.timer.setText('00:00:00')
            self.ui.timer_details.setText('00:00:00')
        elif response_json['state'] == 'preparation':
            current_time = datetime.now(tz=timezone.utc)

            war_start = response_json['startTime']
            war_start_parsed = parser.parse(war_start)
            self.ui.war_prep_end_label.setText('Prep End')

            time_left = war_start_parsed - current_time

        def countdown(time_left):
            while loop_closed == False and stacked_widget.currentIndex() == 4:
                time_left = time_left - timedelta(seconds=1)

                if str(time_left).split('.')[0] != '00:00:00' or 'day' in str(time_left):
                    self.ui.timer.setText(str(time_left).split('.')[0])
                    self.ui.timer_details.setText(str(time_left).split('.')[0])
                    time.sleep(1)
                else:
                    self.ui.timer.setText('00:00:00')
                    break

        try:
            t1 = threading.Thread(target=countdown, args=[time_left])
            t1.start()
        except:
            pass

        self.ui.clan_name_1.setText(response_json[clan_status]['name'])
        self.ui.clan_name_2.setText(response_json[opponent_status]['name'])

        try:
            attacks_per_member = response_json['attacksPerMember']
        except:
            attacks_per_member = 1

        self.ui.attacks_left_1.setText(str(response_json[clan_status]['attacks']) + '/' + str(response_json['teamSize'] * attacks_per_member))
        self.ui.attacks_left_2.setText(str(response_json[opponent_status]['attacks']) + '/' + str(response_json['teamSize'] * attacks_per_member))

        clan_image_response = requests.get(response_json[clan_status]['badgeUrls']['large'])

        if clan_image_response.status_code == 200:
            image_bytes = io.BytesIO(clan_image_response.content)
            img = Image.open(image_bytes)
            clan_qimage = ImageQt(img)

            self.ui.clan_image_1.setPixmap(QtGui.QPixmap.fromImage(clan_qimage))

        opponent_image_response = requests.get(response_json[opponent_status]['badgeUrls']['large'])

        if opponent_image_response.status_code == 200:
            image_bytes = io.BytesIO(opponent_image_response.content)
            img = Image.open(image_bytes)
            opponent_qimage = ImageQt(img)

            self.ui.clan_image_2.setPixmap(QtGui.QPixmap.fromImage(opponent_qimage))

        self.ui.star_count_1.setText(str(response_json[clan_status]['stars']))
        self.ui.star_count_2.setText(str(response_json[opponent_status]['stars']))

        #more details box
        try:
            self.ui.details_clan_name.setText(response_json[clan_status]['name'])
            self.ui.details_opponent_name.setText(response_json[opponent_status]['name'])

            self.ui.details_clan_image_1.setPixmap(QtGui.QPixmap.fromImage(clan_qimage))
            self.ui.details_clan_image_2.setPixmap(QtGui.QPixmap.fromImage(opponent_qimage))

            self.ui.details_clan_star_count.setText(str(response_json[clan_status]['stars']))
            self.ui.details_opponent_star_count.setText(str(response_json[opponent_status]['stars']))

            self.ui.total_clan_percentage.setText(str(round(response_json[clan_status]['destructionPercentage'], 2)) + '%')
            self.ui.total_opponent_percentage.setText(str(round(response_json[opponent_status]['destructionPercentage'], 2)) + '%')

            clan_total_percentage = 0
            clan_hits = 0
            clan_total_time = 0
            clan_stars = []

            opponent_total_percentage = 0
            opponent_hits = 0
            opponent_total_time = 0
            opponent_stars = []

            for i in range(response_json['teamSize']):
                if response_json[opponent_status]['members'][i]['opponentAttacks'] > 0:
                    clan_total_percentage += response_json[opponent_status]['members'][i]['bestOpponentAttack']['destructionPercentage']
                    clan_total_time += response_json[opponent_status]['members'][i]['bestOpponentAttack']['duration']
                    clan_stars.append(response_json[opponent_status]['members'][i]['bestOpponentAttack']['stars'])
                    clan_hits += 1

                if response_json[clan_status]['members'][i]['opponentAttacks'] > 0:
                    opponent_total_percentage += response_json[clan_status]['members'][i]['bestOpponentAttack']['destructionPercentage']
                    opponent_total_time += response_json[clan_status]['members'][i]['bestOpponentAttack']['duration']
                    opponent_stars.append(response_json[clan_status]['members'][i]['bestOpponentAttack']['stars'])
                    opponent_hits += 1

            try:
                clan_average_percentage = clan_total_percentage / clan_hits
                clan_average_time = clan_total_time / clan_hits
            except:
                clan_average_percentage = 0
                clan_average_time = 0
            try:
                opponent_average_percentage = opponent_total_percentage / opponent_hits
                opponent_average_time = opponent_total_time / opponent_hits
            except:
                opponent_average_percentage = 0
                opponent_average_time = 0

            self.ui.average_clan_percentage.setText(str(round(clan_average_percentage, 2)) + '%')
            self.ui.average_opponent_percentage.setText(str(round(opponent_average_percentage, 2)) + '%')

            self.ui.average_clan_time.setText(str(int(clan_average_time // 60)) + 'm ' + str(int(clan_average_time % 60)) + 's')
            self.ui.average_opponent_time.setText(str(int(opponent_average_time // 60)) + 'm ' + str(int(opponent_average_time % 60)) + 's')

            self.ui.clan_three_stars.setText(str(clan_stars.count(3)))
            self.ui.clan_two_stars.setText(str(clan_stars.count(2)))
            self.ui.clan_one_stars.setText(str(clan_stars.count(1)))
            self.ui.clan_zero_stars.setText(str(clan_stars.count(0)))

            self.ui.opponent_three_stars.setText(str(opponent_stars.count(3)))
            self.ui.opponent_two_stars.setText(str(opponent_stars.count(2)))
            self.ui.opponent_one_stars.setText(str(opponent_stars.count(1)))
            self.ui.opponent_zero_stars.setText(str(opponent_stars.count(0)))

            clan_bases_stars = []
            opponent_bases_stars = []
            clan_bases_percent = []
            opponent_bases_percent = []

            for i in range(response_json['teamSize']):
                try:
                    if response_json[clan_status]['members'][i]['bestOpponentAttack']['stars'] == 3:
                        pass
                    elif response_json[clan_status]['members'][i]['bestOpponentAttack']['stars'] == 2:
                        clan_bases_stars.append(1)
                        clan_bases_percent.append(100 - response_json[clan_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                    elif response_json[clan_status]['members'][i]['bestOpponentAttack']['stars'] == 1:
                        clan_bases_stars.append(2)
                        clan_bases_percent.append(100 - response_json[clan_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                    else:
                        clan_bases_stars.append(3)
                        clan_bases_percent.append(100 - response_json[clan_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                except:
                    clan_bases_stars.append(3)
                    clan_bases_percent.append(100)

            for i in range(response_json['teamSize']):
                try:
                    if response_json[opponent_status]['members'][i]['bestOpponentAttack']['stars'] == 3:
                        pass
                    elif response_json[opponent_status]['members'][i]['bestOpponentAttack']['stars'] == 2:
                        opponent_bases_stars.append(1)
                        opponent_bases_percent.append(100 - response_json[opponent_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                    elif response_json[opponent_status]['members'][i]['bestOpponentAttack']['stars'] == 1:
                        opponent_bases_stars.append(2)
                        opponent_bases_percent.append(100 - response_json[opponent_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                    else:
                        opponent_bases_stars.append(3)
                        opponent_bases_percent.append(100 - response_json[opponent_status]['members'][i]['bestOpponentAttack']['destructionPercentage'])
                except:
                    opponent_bases_stars.append(3)
                    opponent_bases_percent.append(100)
            
            clan_bases_stars.sort(reverse=True)
            opponent_bases_stars.sort(reverse=True)
            clan_bases_percent.sort(reverse=True)
            opponent_bases_percent.sort(reverse=True)

            try:
                total_attacks = response_json['teamSize'] * response_json['attacksPerMember']
            except:
                total_attacks = response_json['teamSize']

            opponent_attacks_left = total_attacks - response_json[opponent_status]['attacks']
            opponent_potential_stars = 0
            opponent_potential_percent = 0

            clan_attacks_left = total_attacks - response_json[clan_status]['attacks']
            clan_potential_stars = 0
            clan_potential_percent = 0

            #calculates maximum potential stars clan can get

            for i in range(clan_attacks_left):
                try:
                    clan_potential_stars += opponent_bases_stars[i]
                    clan_potential_percent += opponent_bases_percent[i]
                except:
                    break

            opponent_required_stars = (response_json[clan_status]['stars'] + clan_potential_stars) - response_json[opponent_status]['stars'] + 1
            opponent_required_percent = ((response_json[clan_status]['destructionPercentage'] * response_json['teamSize']) + clan_potential_percent) - (response_json[opponent_status]['destructionPercentage'] * response_json['teamSize']) + 1
            if opponent_required_stars >= 0:
                self.ui.opponent_required_stars.setText(str(opponent_required_stars))
            else:
                self.ui.opponent_required_stars.setText('0')
            if opponent_required_percent >= 0:
                self.ui.opponent_required_percent.setText(str(round(opponent_required_percent, 1)) + '%')
            else:
                self.ui.opponent_required_percent.setText('0%')

            #calculates maximum potential stars opponent can get

            for i in range(opponent_attacks_left):
                try:
                    opponent_potential_stars += clan_bases_stars[i]
                    opponent_potential_percent += clan_bases_percent[i]
                except:
                    break

            clan_required_stars = (response_json[opponent_status]['stars'] + opponent_potential_stars) - response_json[clan_status]['stars'] + 1
            clan_required_percent = ((response_json[opponent_status]['destructionPercentage'] * response_json['teamSize']) + opponent_potential_percent) - (response_json[clan_status]['destructionPercentage'] * response_json['teamSize']) + 1
            if clan_required_stars >= 0:
                self.ui.clan_required_stars.setText(str(clan_required_stars))
            else:
                self.ui.clan_required_stars.setText('0')
            if clan_required_percent >= 0:
                self.ui.clan_required_percent.setText(str(round(clan_required_percent, 1)) + '%')
            else:
                self.ui.clan_required_percent.setText('0%')

            for object in self.ui.war_participants_box.children():
                object.show()

            boxes_to_hide = 50 - response_json['teamSize']
            
            # hide boxes of friendly team
            for i in range(boxes_to_hide):
                self.ui.war_participants_box.children()[len(self.ui.war_participants_box.children()) - 51 - i].hide()

            #hide boxes of enemy team
            for i in range(boxes_to_hide):
                self.ui.war_participants_box.children()[len(self.ui.war_participants_box.children()) - i - 1].hide()

            #set appropriate size
            self.ui.war_participants_box.setMinimumHeight(2550 - (boxes_to_hide * 50))
        except:
            pass
    
    def load_war_participants(self, response_json, clan_status, opponent_status, participants):
        clan_loop_status = clan_status
        opponent_loop_status = opponent_status

        try:
            attacks_per_member = response_json['attacksPerMember']
        except:
            attacks_per_member = 1

        participants[clan_status].sort(key=lambda d: d['mapPosition'])
        participants[opponent_status].sort(key=lambda d: d['mapPosition'])

        for i in range(response_json['teamSize']):
            participants['clan'][i].update({'mapPosition': i + 1})
        for i in range(response_json['teamSize']):
            participants['opponent'][i].update({'mapPosition': i + 1})

        for _ in range(2):
            for i in range(response_json['teamSize']):

                total_stars = 0
                total_percent = 0
                dips = 0
                
                try:
                    for attacks in participants[clan_loop_status][i]['attacks']:
                        total_stars += attacks['stars']
                        total_percent += attacks['destructionPercentage']

                        opponent_tag = attacks['defenderTag']

                        def find_opponent_town_hall_level():
                            for member in participants[opponent_loop_status]:
                                if member['tag'] == opponent_tag:
                                    return member['townhallLevel']
                        
                        def find_opponent_map_position():
                            for member in participants[opponent_loop_status]:
                                if member['tag'] == opponent_tag:
                                    return member['mapPosition']
                        
                        attacks.update({'opponent_townhall_level': find_opponent_town_hall_level(), 'opponent_map_position': find_opponent_map_position()})

                        dips += participants[clan_loop_status][i]['townhallLevel'] - find_opponent_town_hall_level()
                except:
                    pass

                try:
                    opponent_attack = participants[clan_loop_status][i]['bestOpponentAttack']

                    best_opponent_tag = opponent_attack['attackerTag']

                    def find_best_opponent_town_hall_level():
                        for member in participants[opponent_loop_status]:
                            if member['tag'] == best_opponent_tag:
                                return member['townhallLevel']
                    
                    def find_best_opponent_map_position():
                        for member in participants[opponent_loop_status]:
                            if member['tag'] == best_opponent_tag:
                                return member['mapPosition']
                    
                    opponent_attack.update({'opponent_townhall_level': find_best_opponent_town_hall_level(), 'opponent_map_position': find_best_opponent_map_position()})
                except:
                    pass
                
                try:
                    defence_stars = participants[clan_loop_status][i]['bestOpponentAttack']['stars']
                    defence_percent = participants[clan_loop_status][i]['bestOpponentAttack']['destructionPercentage']
                except:
                    defence_stars = 0
                    defence_percent = 0
                
                try:
                    attacks_left = attacks_per_member - len(participants[clan_loop_status][i]['attacks'])
                except:
                    attacks_left = attacks_per_member

                if attacks_left > 0:
                    color = '#ad0014'
                else:
                    color = 'black'

                participants[clan_loop_status][i].update({'dips': dips, 'total_stars': total_stars, 'total_percent': total_percent, 'defence_stars': defence_stars, 'defence_percent': defence_percent, 'color': color})
                
            clan_loop_status = opponent_status
            opponent_loop_status = clan_status
        
        self.show_war_participants(response_json, participants)
        
        self.ui.friendly_more_info_button_00.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 0))
        self.ui.friendly_more_info_button_01.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 1))
        self.ui.friendly_more_info_button_02.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 2))
        self.ui.friendly_more_info_button_03.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 3))
        self.ui.friendly_more_info_button_04.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 4))
        self.ui.friendly_more_info_button_05.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 5))
        self.ui.friendly_more_info_button_06.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 6))
        self.ui.friendly_more_info_button_07.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 7))
        self.ui.friendly_more_info_button_08.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 8))
        self.ui.friendly_more_info_button_09.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 9))
        self.ui.friendly_more_info_button_10.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 10))
        self.ui.friendly_more_info_button_11.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 11))
        self.ui.friendly_more_info_button_12.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 12))
        self.ui.friendly_more_info_button_13.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 13))
        self.ui.friendly_more_info_button_14.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 14))
        self.ui.friendly_more_info_button_15.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 15))
        self.ui.friendly_more_info_button_16.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 16))
        self.ui.friendly_more_info_button_17.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 17))
        self.ui.friendly_more_info_button_18.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 18))
        self.ui.friendly_more_info_button_19.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 19))
        self.ui.friendly_more_info_button_20.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 20))
        self.ui.friendly_more_info_button_21.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 21))
        self.ui.friendly_more_info_button_22.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 22))
        self.ui.friendly_more_info_button_23.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 23))
        self.ui.friendly_more_info_button_24.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 24))
        self.ui.friendly_more_info_button_25.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 25))
        self.ui.friendly_more_info_button_26.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 26))
        self.ui.friendly_more_info_button_27.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 27))
        self.ui.friendly_more_info_button_28.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 28))
        self.ui.friendly_more_info_button_29.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 29))
        self.ui.friendly_more_info_button_30.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 30))
        self.ui.friendly_more_info_button_31.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 31))
        self.ui.friendly_more_info_button_32.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 32))
        self.ui.friendly_more_info_button_33.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 33))
        self.ui.friendly_more_info_button_34.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 34))
        self.ui.friendly_more_info_button_35.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 35))
        self.ui.friendly_more_info_button_36.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 36))
        self.ui.friendly_more_info_button_37.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 37))
        self.ui.friendly_more_info_button_38.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 38))
        self.ui.friendly_more_info_button_39.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 39))
        self.ui.friendly_more_info_button_40.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 40))
        self.ui.friendly_more_info_button_41.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 41))
        self.ui.friendly_more_info_button_42.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 42))
        self.ui.friendly_more_info_button_43.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 43))
        self.ui.friendly_more_info_button_44.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 44))
        self.ui.friendly_more_info_button_45.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 45))
        self.ui.friendly_more_info_button_46.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 46))
        self.ui.friendly_more_info_button_47.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 47))
        self.ui.friendly_more_info_button_48.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 48))
        self.ui.friendly_more_info_button_49.clicked.connect(lambda: self.show_more_participant_information(participants, 'clan', 49))

        self.ui.enemy_more_info_button_00.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 0))
        self.ui.enemy_more_info_button_01.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 1))
        self.ui.enemy_more_info_button_02.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 2))
        self.ui.enemy_more_info_button_03.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 3))
        self.ui.enemy_more_info_button_04.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 4))
        self.ui.enemy_more_info_button_05.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 5))
        self.ui.enemy_more_info_button_06.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 6))
        self.ui.enemy_more_info_button_07.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 7))
        self.ui.enemy_more_info_button_08.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 8))
        self.ui.enemy_more_info_button_09.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 9))
        self.ui.enemy_more_info_button_10.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 10))
        self.ui.enemy_more_info_button_11.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 11))
        self.ui.enemy_more_info_button_12.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 12))
        self.ui.enemy_more_info_button_13.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 13))
        self.ui.enemy_more_info_button_14.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 14))
        self.ui.enemy_more_info_button_15.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 15))
        self.ui.enemy_more_info_button_16.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 16))
        self.ui.enemy_more_info_button_17.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 17))
        self.ui.enemy_more_info_button_18.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 18))
        self.ui.enemy_more_info_button_19.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 19))
        self.ui.enemy_more_info_button_20.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 20))
        self.ui.enemy_more_info_button_21.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 21))
        self.ui.enemy_more_info_button_22.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 22))
        self.ui.enemy_more_info_button_23.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 23))
        self.ui.enemy_more_info_button_24.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 24))
        self.ui.enemy_more_info_button_25.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 25))
        self.ui.enemy_more_info_button_26.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 26))
        self.ui.enemy_more_info_button_27.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 27))
        self.ui.enemy_more_info_button_28.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 28))
        self.ui.enemy_more_info_button_29.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 29))
        self.ui.enemy_more_info_button_30.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 30))
        self.ui.enemy_more_info_button_31.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 31))
        self.ui.enemy_more_info_button_32.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 32))
        self.ui.enemy_more_info_button_33.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 33))
        self.ui.enemy_more_info_button_34.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 34))
        self.ui.enemy_more_info_button_35.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 35))
        self.ui.enemy_more_info_button_36.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 36))
        self.ui.enemy_more_info_button_37.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 37))
        self.ui.enemy_more_info_button_38.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 38))
        self.ui.enemy_more_info_button_39.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 39))
        self.ui.enemy_more_info_button_40.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 40))
        self.ui.enemy_more_info_button_41.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 41))
        self.ui.enemy_more_info_button_42.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 42))
        self.ui.enemy_more_info_button_43.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 43))
        self.ui.enemy_more_info_button_44.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 44))
        self.ui.enemy_more_info_button_45.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 45))
        self.ui.enemy_more_info_button_46.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 46))
        self.ui.enemy_more_info_button_47.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 47))
        self.ui.enemy_more_info_button_48.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 48))
        self.ui.enemy_more_info_button_49.clicked.connect(lambda: self.show_more_participant_information(participants, 'opponent', 49))

        self.ui.friendly_war_position_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'mapPosition', None, 'clan', response_json))
        self.ui.friendly_stars_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'total_stars', 'total_percent', 'clan', response_json))
        self.ui.friendly_defence_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'defence_stars', 'defence_percent', 'clan', response_json))
        self.ui.friendly_dips_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'dips', None, 'clan', response_json))

        self.ui.enemy_war_position_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'mapPosition', None, 'opponent', response_json))
        self.ui.enemy_stars_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'total_stars', 'total_percent', 'opponent', response_json))
        self.ui.enemy_defence_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'defence_stars', 'defence_percent', 'opponent', response_json))
        self.ui.enemy_dips_sort_button.clicked.connect(lambda: self.sort_participants(participants, 'dips', None, 'opponent', response_json))

    def show_war_participants(self, response_json, participants):
        add_fifty = 0
        clan_loop_status = 'clan'

        for _ in range(2):
            for i in range(response_json['teamSize']):
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[0].setText(str(participants[clan_loop_status][i]['mapPosition']))
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[3].setText(participants[clan_loop_status][i]['name'])
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[3].setStyleSheet('border: 0px;\n'
'background: none;\n'
'color: ' + participants[clan_loop_status][i]['color'])
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[2].setStyleSheet('border-image: url(:/members/townhall' + str(participants[clan_loop_status][i]['townhallLevel']) + '.png);')
                
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[5].setText(str(participants[clan_loop_status][i]['total_stars']))
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[6].setText(str(participants[clan_loop_status][i]['total_percent']) + '%')
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[11].setText(str(participants[clan_loop_status][i]['dips']))

                self.ui.war_participants_box.children()[i+2+add_fifty].children()[8].setText(str(participants[clan_loop_status][i]['defence_stars']))
                self.ui.war_participants_box.children()[i+2+add_fifty].children()[10].setText(str(participants[clan_loop_status][i]['defence_percent']) + '%')
            
            add_fifty += 50
            clan_loop_status = 'opponent'
    
    def sort_participants(self, participants, key, key2, status, response_json):
        if key2 == None:
            new_participants = sorted(participants[status], key=lambda d: d[key], reverse=True)

            if new_participants == participants[status]:
                participants[status].sort(key=lambda d: d[key])
            else:
                participants[status].sort(key=lambda d: d[key], reverse=True)
        else:
            new_participants = sorted(participants[status], key=lambda d: (d[key], d[key2]), reverse=True)
            if new_participants == participants[status]:
                participants[status].sort(key=lambda d: (d[key], d[key2]))
            else:
                participants[status].sort(key=lambda d: (d[key], d[key2]), reverse=True)
                
        self.show_war_participants(response_json, participants)
    
    def show_more_participant_information(self, participants, status, index):
        all_users = db.child('users').get().val()
        player = participants[status][index]
        player_tag = participants[status][index]['tag'].lstrip('#')

        for user in all_users:
            if user['tag'] == player_tag:
                user_db = user
                break

        self.ui.participant_name.setText(player['name'])
        
        try: #attack 1
            attack_1 = player['attacks'][0]
            self.ui.attack_1_participant_war_position.setText(str(player['mapPosition']))
            self.ui.attack_1_opponent_war_position.setText(str(attack_1['opponent_map_position']))

            self.ui.attack_1_participant_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(player['townhallLevel']) + '.png);')
            self.ui.attack_1_opponent_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(attack_1['opponent_townhall_level']) + '.png);')

            self.ui.attack_1_stars.setText(str(attack_1['stars']))
            self.ui.attack_1_percentage.setText(str(attack_1['destructionPercentage']) + '%')
            if len(str(attack_1['duration'] % 60)) == 1:
                duration_seconds = '0' + str(attack_1['duration'] % 60)
            else:
                duration_seconds = str(attack_1['duration'] % 60)
            self.ui.attack_1_time.setText(str(attack_1['duration'] // 60) + ':' + duration_seconds)

            self.ui.attack_1_not_found.hide()
            self.ui.attack_1_participant_war_position.show()
            self.ui.attack_1_opponent_war_position.show()
            self.ui.attack_1_participant_town_hall.show()
            self.ui.attack_1_opponent_town_hall.show()
            self.ui.attack_1_stars.show()
            self.ui.attack_1_percentage.show()
            self.ui.attack_1_time.show()
            self.ui.attack_1_vs_label.show()
            self.ui.attack_1_star_image.show()
            self.ui.participant_information_line_3.show()
        except:
            self.ui.attack_1_not_found.show()
            self.ui.attack_1_participant_war_position.hide()
            self.ui.attack_1_opponent_war_position.hide()
            self.ui.attack_1_participant_town_hall.hide()
            self.ui.attack_1_opponent_town_hall.hide()
            self.ui.attack_1_stars.hide()
            self.ui.attack_1_percentage.hide()
            self.ui.attack_1_time.hide()
            self.ui.attack_1_vs_label.hide()
            self.ui.attack_1_star_image.hide()
            self.ui.participant_information_line_3.hide()
        
        try: #attack 2
            attack_2 = player['attacks'][1]
            self.ui.attack_2_participant_war_position.setText(str(player['mapPosition']))
            self.ui.attack_2_opponent_war_position.setText(str(attack_2['opponent_map_position']))

            self.ui.attack_2_participant_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(player['townhallLevel']) + '.png);')
            self.ui.attack_2_opponent_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(attack_2['opponent_townhall_level']) + '.png);')

            self.ui.attack_2_stars.setText(str(attack_2['stars']))
            self.ui.attack_2_percentage.setText(str(attack_2['destructionPercentage']) + '%')
            if len(str(attack_2['duration'] % 60)) == 1:
                duration_seconds = '0' + str(attack_2['duration'] % 60)
            else:
                duration_seconds = str(attack_2['duration'] % 60)

            self.ui.attack_2_time.setText(str(attack_2['duration'] // 60) + ':' + duration_seconds)

            self.ui.attack_2_not_found.hide()
            self.ui.attack_2_participant_war_position.show()
            self.ui.attack_2_opponent_war_position.show()
            self.ui.attack_2_participant_town_hall.show()
            self.ui.attack_2_opponent_town_hall.show()
            self.ui.attack_2_stars.show()
            self.ui.attack_2_percentage.show()
            self.ui.attack_2_time.show()
            self.ui.attack_2_vs_label.show()
            self.ui.attack_2_star_image.show()
            self.ui.participant_information_line_11.show()
        except:
            self.ui.attack_2_not_found.show()
            self.ui.attack_2_participant_war_position.hide()
            self.ui.attack_2_opponent_war_position.hide()
            self.ui.attack_2_participant_town_hall.hide()
            self.ui.attack_2_opponent_town_hall.hide()
            self.ui.attack_2_stars.hide()
            self.ui.attack_2_percentage.hide()
            self.ui.attack_2_time.hide()
            self.ui.attack_2_vs_label.hide()
            self.ui.attack_2_star_image.hide()
            self.ui.participant_information_line_11.hide()
        
        try: #best defence 
            opponent_attack = player['bestOpponentAttack']
            self.ui.best_defence_participant_war_position.setText(str(player['mapPosition']))
            self.ui.best_defence_opponent_war_position.setText(str(opponent_attack['opponent_map_position']))

            self.ui.best_defence_participant_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(player['townhallLevel']) + '.png);')
            self.ui.best_defence_opponent_town_hall.setStyleSheet('border-image: url(:/members/townhall' + str(opponent_attack['opponent_townhall_level']) + '.png);')

            self.ui.best_defence_stars.setText(str(opponent_attack['stars']))
            self.ui.best_defence_percentage.setText(str(opponent_attack['destructionPercentage']) + '%')
            if len(str(opponent_attack['duration'] % 60)) == 1:
                duration_seconds = '0' + str(opponent_attack['duration'] % 60)
            else:
                duration_seconds = str(opponent_attack['duration'] % 60)
            self.ui.best_defence_time.setText(str(opponent_attack['duration'] // 60) + ':' + duration_seconds)

            self.ui.best_defence_not_found.hide()
            self.ui.best_defence_participant_war_position.show()
            self.ui.best_defence_opponent_war_position.show()
            self.ui.best_defence_participant_town_hall.show()
            self.ui.best_defence_opponent_town_hall.show()
            self.ui.best_defence_stars.show()
            self.ui.best_defence_percentage.show()
            self.ui.best_defence_time.show()
            self.ui.best_defence_vs_label.show()
            self.ui.best_defence_star_image.show()
        except:
            self.ui.best_defence_not_found.show()
            self.ui.best_defence_participant_war_position.hide()
            self.ui.best_defence_opponent_war_position.hide()
            self.ui.best_defence_participant_town_hall.hide()
            self.ui.best_defence_opponent_town_hall.hide()
            self.ui.best_defence_stars.hide()
            self.ui.best_defence_percentage.hide()
            self.ui.best_defence_time.hide()
            self.ui.best_defence_vs_label.hide()
            self.ui.best_defence_star_image.hide()

        try: #previous war stats
      
            if len(user_db['warstats']) <= 7:
                loop_number = len(user['warstats'])
            else:
                loop_number = 7
            
            total_stars = 0
            total_percent = 0

            total_defence_stars = 0
            total_defence_percent = 0

            total_dips = 0
            missed_hits = 0

            total_attacks = 0

            for war in list(reversed(user_db['warstats'])):
                total_stars += war['total_stars']
                total_percent += war['total_percent']

                total_defence_stars += war['defence_stars']
                total_defence_percent += war['defence_percent']

                total_dips += war['dips']
                missed_hits += war['missed_hits']

                try:
                    total_attacks += len(war['attacks'])
                except:
                    pass
            
            if total_attacks > 0:
                average_stars = round(total_stars / total_attacks, 2)
                average_percent = round(total_percent / total_attacks, 2)

                average_defence_stars = round(total_defence_stars / total_attacks, 2)
                average_defence_percent = round(total_defence_percent / total_attacks, 2)

                average_dips = round(total_dips / total_attacks, 2)
            else:
                average_stars = 0
                average_percent = 0

                average_defence_stars = 0
                average_defence_percent = 0

                average_dips = 0

            self.ui.previous_wars_label.setText(f'Previous {loop_number} War Stats')
            self.ui.average_stars.setText(f'Average Stars: {average_stars}')
            self.ui.average_percent.setText(f'Average Percent: {average_percent}%')
            self.ui.average_defence_stars.setText(f'Average Defence Stars: {average_defence_stars}')
            self.ui.average_defence_percent.setText(f'Average Defence Percent: {average_defence_percent}%')
            self.ui.average_dips.setText(f'Average Dips: {average_dips}')
            self.ui.missed_hits.setText(f'Missed Hits: {missed_hits}')

            self.ui.average_stars.show()
            self.ui.average_percent.show()
            self.ui.average_defence_stars.show()
            self.ui.average_defence_percent.show()
            self.ui.average_dips.show()
            self.ui.missed_hits.show()
            self.ui.db_info_not_found.hide()
            
        except:
            self.ui.previous_wars_label.setText('Previous 0 War Stats')
            self.ui.average_stars.hide()
            self.ui.average_percent.hide()
            self.ui.average_defence_stars.hide()
            self.ui.average_defence_percent.hide()
            self.ui.average_dips.hide()
            self.ui.missed_hits.hide()
            self.ui.db_info_not_found.show()

        self.ui.participant_information_box.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    stacked_widget = QtWidgets.QStackedWidget()

    screen1 = TitleScreen()
    screen2 = AddClanScreen()
    screen3 = selectionFunctionScreen()
    screen4 = membersScreen()
    screen5 = warCwlScreen()

    stacked_widget.addWidget(screen1)
    stacked_widget.addWidget(screen2)
    stacked_widget.addWidget(screen3)
    stacked_widget.addWidget(screen4)
    stacked_widget.addWidget(screen5)

    stacked_widget.setFixedWidth(1070)
    stacked_widget.setFixedHeight(720)

    stacked_widget.setWindowTitle('Clash Clan Manager')

    path = os.path.dirname(os.path.abspath(__file__))
    stacked_widget.setWindowIcon(QtGui.QIcon(path + '/Game Graphics/CCM logo circle.png'))

    stacked_widget.show()
    def close_loop():
        global loop_closed
        loop_closed = True

    app.aboutToQuit.connect(close_loop)
    sys.exit(app.exec_())
