#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from urllib.request import urlopen as get

from PyQt5.QtGui import QIcon, QPixmap


class IconTool(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def buildQIcon(name):
        file = os.path.join('..', 'resources', 'images', name)
        return QIcon(file)

    @staticmethod
    def buildQPixmap(name):
        file = os.path.join('..', 'resources', 'images', name)
        return QPixmap(file)

    @staticmethod
    def imgFromUrl(url):
        with get(url) as response:
            _map = QPixmap()
            d = response.read()
            _map.loadFromData(d)
        return _map
