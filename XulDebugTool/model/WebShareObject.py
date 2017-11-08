#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Web桥接对象
author: Allen
last edited: 2017.11.7

"""
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget, QMessageBox


class WebShareObject(QWidget):
    def __init__(self):
        super(WebShareObject, self).__init__()

    def _getStrValue(self):
        print('页面获取参数')
        return '100'

    def _setStrValue(self, str):
        print('页面接受参数:%s' % str)
        QMessageBox.information(self, "Information", '获得页面参数 ：%s' % str)

    strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue)
