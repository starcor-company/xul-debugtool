import json
import threading
from PyQt5 import QtCore

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel

from XulDebugTool.logcatapi.Logcat import STCLogger
from XulDebugTool.ui.widget.FavoriteTreeView import FavoriteTreeView
from XulDebugTool.ui.widget.UpdateProperty import UpdateProperty
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper


def illegal(url):
    blacklist = (
        "@color:"
    )
    for e in blacklist:
        if url.startswith(e):
            return True
    return False


class RightArea(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image = QLabel()
        self.__initImgWidget(self.image)
        tab = QTabWidget()
        self.favorite = FavoriteTreeView(self)
        self.prop = UpdateProperty()
        self.__initTabWidget(tab, self.favorite, self.prop)

        self.__setLayout(tab, self.image)

    def __initImgWidget(self, img):
        img.setAutoFillBackground(True)
        img.setMaximumHeight(300)

    def __setLayout(self, tab, img):
        layout = QVBoxLayout()
        layout.addWidget(tab)
        layout.addWidget(img)
        self.setLayout(layout)

    def __initTabWidget(self, tab, favorite, prop):
        tab.setTabPosition(QTabWidget.East)
        tab.addTab(prop, IconTool.buildQIcon('property.png'), 'Property')
        tab.setStyleSheet(('QTab::tab{height:60px;width:32px;color:black;padding:0px}'
                           'QTabBar::tab:selected{background:lightgray}'))
        tab.addTab(favorite, IconTool.buildQIcon('favorites.png'), 'Favorites')

    def updateProp(self, value=None):
        p = self.prop
        print('this is {} value is {}'.format(str(p), value[:50]))
        p.initData(value)
        p.updateAttrUI()
        p.updateStyleUI()

    def onGetQueryUrl(self, url):
        STCLogger().i('onGetQueryUrl url:' + url)
        self.favorite.updateTree()
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)

    def showImage(self, event):
        e = self.__parseEvent(event)
        if e['isAssets']:
            task = self.__showImgByAssets
        else:
            task = self.__showImgByUrl

        if not illegal(e['url']):
            threading.Thread(target=task, args=(e['url'],)).start()

    def __parseEvent(self, event):
        e = json.loads(event)
        d = e["data"]
        r = {
            "prefix": "",
            "isAssets": False,
            "url": d,
        }
        prefix = self.__PREFIX()

        for p in prefix:
            if d.startswith(p):
                r['url'] = d.replace(p, "", 1)
                r['prefix'] = p
                break
        r['isAssets'] = r['url'].startswith("file:///.assets")

        return r

    def __PREFIX(self):
        p = (
            "effect:mirror:",
            "effect:hexagon:",
            "effect:parallelogram:",
            "effect:blur:",
            "effect:polygon:",
            "effect:circle:",
            "scale:",
            "mgtv_scale:",
            "sift:",
            "@gradient:",
            "colors:",
            "radii:",
            "qrCode:",
            "native_file:",
        )
        return p

    def __showImgByUrl(self, url):
        iw = self.image
        img = IconTool.imgFromUrl(url)
        img = img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        print('showImgTask {}'.format(img))
        iw.setPixmap(img)

    def __showImgByAssets(self, path):
        d = XulDebugServerHelper.getAssets(path)
        _map = QPixmap()
        _map.loadFromData(d)
        _map = _map.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        print('showImgTask {}'.format(_map))

        iw = self.image
        iw.setPixmap(_map)
