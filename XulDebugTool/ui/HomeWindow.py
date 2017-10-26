#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/20 17:41
# @Author  : Mrlsm -- starcor


from PyQt5.QtWidgets import QAction
from PyQt5.uic.properties import QtWidgets, QtGui

from XulDebugTool.ui.BaseWindow import BaseWindow


MENU = ['File', 'Edit', 'Adb', 'Help']

class HomeWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setFixedSize(820, 640)
        self.initMenuBar()

    def initMenuBar(self):
        self.statusBar()
        menubar = self.menuBar()
        # file栏
        fileMenu = menubar.addMenu('&File')

        disconAction = QAction( '&Disconnect', self)
        disconAction.setStatusTip('disconnect your devices！')
        disconAction.triggered.connect(self.disconnect)

        settingAction = QAction('&Setting', self)
        settingAction.setStatusTip('Setting！')
        settingAction.triggered.connect(self.setting)

        contAction = QAction('&Controller', self)
        contAction.setStatusTip('Controller！')
        contAction.triggered.connect(self.disconnect)

        fileMenu.addAction(disconAction)
        fileMenu.addAction(settingAction)
        fileMenu.addAction(contAction)

    def disconnect(self):
        print("disconnect!!!")

    def setting(self):
        print("setting!!!")
