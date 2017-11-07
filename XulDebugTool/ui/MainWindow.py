#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XulDebugTool

主页面

author: Kenshin
last edited: 2017.10.23
"""

import pyperclip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

from XulDebugTool.ui.BaseWindow import BaseWindow
from XulDebugTool.ui.widget.ConsoleView import ConsoleWindow
from XulDebugTool.ui.widget.PropertyEditor import PropertyEditor
from XulDebugTool.ui.widget.SearchBarQLineEdit import SearchBarQLineEdit
from XulDebugTool.utils.IconTool import IconTool
from XulDebugTool.utils.Utils import Utils
from XulDebugTool.utils.XulDebugServerHelper import XulDebugServerHelper

ROOT_ITEM_PAGE = 'Page'
ROOT_ITEM_USER_OBJECT = 'User-Object'
ROOT_ITEM_PLUGIN = 'Plugin'
CHILD_ITEM_DATA_SERVICE = 'DataService'


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.initConsole()
        self.initUI()
        self.show()

    def initConsole(self):
        self.consoleView = ConsoleWindow()

    def initUI(self):
        self.resize(1400, 800)
        self.initMenuBar()
        self.initLayout()
        super().initWindow()

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        disConnectAction = QAction(IconTool.buildQIcon('disconnect.png'), 'Disconnect', self)
        disConnectAction.setShortcut('Ctrl+D')
        settingAction = QAction(IconTool.buildQIcon('setting.png'), 'Setting...', self)
        settingAction.setShortcut('Ctrl+Shift+S')
        showLogAction = QAction('Show Log', self)
        fileMenu.addAction(disConnectAction)
        fileMenu.addAction(settingAction)
        fileMenu.addAction(showLogAction)

        editMenu = menuBar.addMenu('Edit')
        findAction = QAction(IconTool.buildQIcon('find.png'), 'Find', self)
        findAction.setShortcut('Ctrl+F')
        editMenu.addAction(findAction)

        helpMenu = menuBar.addMenu('Help')
        aboutAction = QAction(IconTool.buildQIcon('about.png'), 'About', self)
        helpMenu.addAction(aboutAction)

    def initLayout(self):
        # ----------------------------left layout---------------------------- #
        self.treeModel = QStandardItemModel()
        self.pageItem = QStandardItem(ROOT_ITEM_PAGE)
        self.buildPageItem()
        self.userobjectItem = QStandardItem(ROOT_ITEM_USER_OBJECT)
        self.buildUserObjectItem()
        self.pluginItem = QStandardItem(ROOT_ITEM_PLUGIN)
        self.treeModel.appendColumn([self.pageItem, self.userobjectItem, self.pluginItem])
        self.treeModel.setHeaderData(0, Qt.Horizontal, 'Model')

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openContextMenu)
        self.treeView.clicked.connect(self.getDebugData)

        leftContainer = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 6, 0)  # left, top, right, bottom
        layout.addWidget(self.treeView)
        leftContainer.setLayout(layout)

        # ----------------------------middle layout---------------------------- #
        middleContainer = QWidget()
        middleContainer.toggleSidebarsButton = QPushButton()
        middleContainer.toggleSidebarsButton.setToolTip('Hide / show the sidebars')
        middleContainer.toggleSidebarsButton.setIcon(IconTool.buildQIcon('toggle_sidebars.png'))
        middleContainer.toggleSidebarsButton.setStyleSheet('QPushButton {\
            width: 22px;\
            height: 22px;\
            padding: 5px; }')
        # middleContainer.toggle_sidebars_button.clicked.connect(self.toggle_sidebars)

        middleContainer.searchBar = SearchBarQLineEdit(self)
        middleContainer.searchBar.setPlaceholderText('Search')
        middleContainer.searchBar.setMaximumWidth(300)
        middleContainer.searchBar.setMaximumHeight(32)
        middleContainer.searchBar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        # search shall start not before the user completed typing
        # filter_delay = DelayedExecutionTimer(self)
        # new_column.search_bar.textEdited[str].connect(filter_delay.trigger)
        # filter_delay.triggered[str].connect(self.search)

        self.tabBar = QTabBar()
        self.tabBar.setUsesScrollButtons(False)
        self.tabBar.setDrawBase(False)
        self.tabBar.addTab('tab1')
        self.tabBar.addTab('tab2')

        self.pathBar = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.pathBar.setLayout(layout)

        self.searchHolder = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.tabBar)
        layout.addWidget(self.pathBar)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        layout.addWidget(middleContainer.searchBar)
        layout.addWidget(middleContainer.toggleSidebarsButton)
        layout.setStretchFactor(middleContainer.searchBar, 1)
        self.searchHolder.setLayout(layout)
        self.searchHolder.layout().setContentsMargins(6, 6, 6, 0)

        middleContainer.stackedWidget = QStackedWidget()
        self.browser = QWebEngineView()
        self.showXulDebugData(XulDebugServerHelper.HOST + 'list-pages')
        middleContainer.stackedWidget.addWidget(self.browser)
        middleContainer.stackedWidget.addWidget(QLabel('tab2 content'))

        self.tabBar.currentChanged.connect(lambda: middleContainer.stackedWidget.setCurrentIndex(
            self.tabBar.currentIndex()
        ))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.searchHolder)
        layout.addWidget(middleContainer.stackedWidget)
        middleContainer.setLayout(layout)

        # ----------------------------right layout---------------------------- #

        self.propertyEditor = PropertyEditor(['Key', 'Value'])
        def buildProperty():
            qObject = QObject()
            qObject.name = 'xxx'
            qObject.width = 20
            qObject.height = 20
            return qObject
        self.properties = buildProperty()
        self.propertyEditor.addProperty(self.properties)

        rightContainer = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.propertyEditor)
        rightContainer.setLayout(layout)

        # ----------------------------entire layout---------------------------- #

        self.contentSplitter = QSplitter(Qt.Horizontal)
        self.contentSplitter.setHandleWidth(0)  # thing to grab the splitter

        self.contentSplitter.addWidget(leftContainer)
        self.contentSplitter.addWidget(middleContainer)
        self.contentSplitter.addWidget(rightContainer)
        self.contentSplitter.setStretchFactor(0, 0)
        self.contentSplitter.setStretchFactor(1, 6)
        self.contentSplitter.setStretchFactor(2, 6)

        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.setHandleWidth(0)

        self.mainSplitter.addWidget(self.contentSplitter)
        self.mainSplitter.addWidget(self.consoleView)
        self.mainSplitter.setStretchFactor(1, 0)
        self.mainSplitter.setStretchFactor(2,1)
        self.setCentralWidget(self.mainSplitter)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.treeView.indexAt(point)
        if not index.isValid():
            return
        menu = QMenu()
        copyAction = QAction(IconTool.buildQIcon('copy.png'), 'Copy to Clipboard', self,
                             triggered=lambda: pyperclip.copy('%s' % index.data()))
        menu.addAction(copyAction)
        menu.exec_(self.treeView.viewport().mapToGlobal(point))

    @pyqtSlot(QModelIndex)
    def getDebugData(self, index):
        # item = index.internalPointer()
        itemText = index.data()
        parentText = index.parent().data()

        if itemText == ROOT_ITEM_PAGE:  # page节点
            self.buildPageItem()
            self.showXulDebugData(XulDebugServerHelper.HOST + 'list-pages')
        elif itemText == ROOT_ITEM_USER_OBJECT:  # userobject节点
            self.buildUserObjectItem()
            self.showXulDebugData(XulDebugServerHelper.HOST + 'list-user-objects')
        elif itemText == ROOT_ITEM_PLUGIN:  # plugin节点
            pass
        elif parentText == ROOT_ITEM_PAGE:  # page下的子节点
            pageId = itemText[itemText.find('(') + 1:-1]
            self.showXulDebugData(XulDebugServerHelper.HOST + 'get-layout/' + pageId)
        elif parentText == ROOT_ITEM_USER_OBJECT:  # userobject下的子节点
            objectId = itemText[itemText.find('(') + 1:-1]
            self.showXulDebugData(XulDebugServerHelper.HOST + 'get-user-object/' + objectId)

    def buildPageItem(self):
        self.pageItem.removeRows(0, self.pageItem.rowCount())
        r = XulDebugServerHelper.listPages()
        if r:
            pagesNodes = Utils.xml2json(r.data, 'pages')
            if pagesNodes == '':
                return
            # 如果只有一个page,转化出来的json不是数据.分开处理
            if isinstance(pagesNodes['page'], list):
                for i, page in enumerate(pagesNodes['page']):
                    # 把page解析了以后放page节点下
                    row = QStandardItem('%s(%s)' % (page['@pageId'], page['@id']))
                    row.data = page
                    self.pageItem.appendRow(row)
            else:
                page = pagesNodes['page']
                row = QStandardItem('%s(%s)' % (page['@pageId'], page['@id']))
                row.data = page
                self.pageItem.appendRow(row)

    def buildUserObjectItem(self):
        self.userobjectItem.removeRows(0, self.userobjectItem.rowCount())
        r = XulDebugServerHelper.listUserObject()
        if r:
            userObjectNodes = Utils.xml2json(r.data, 'objects')
            # 如果只有一个userObject,转化出来的json不是数据.分开处理
            if isinstance(userObjectNodes['object'], list):
                for i, o in enumerate(userObjectNodes['object']):
                    # 把userObject加到User-Object节点下
                    row = QStandardItem('%s(%s)' % (o['@name'], o['@id']))
                    row.data = o
                    self.userobjectItem.appendRow(row)
                    # 如果是DataServcie, 填充所有的Provider到该节点下
                    if o['@name'] == CHILD_ITEM_DATA_SERVICE:
                        r = XulDebugServerHelper.getUserObject(o['@id'])
                        if r:
                            dataServiceNodes = Utils.xml2json(r.data, 'object')
                            for j, provider in enumerate(dataServiceNodes['object']['provider']):
                                dsRow = QStandardItem(provider['ds']['@providerClass'])
                                row.appendRow(dsRow)
                            # 对Provider按升序排序
                            row.sortChildren(0)
            else:
                o = userObjectNodes['object']
                row = QStandardItem('%s(%s)' % (o['@name'], o['@id']))
                row.data = o
                self.userobjectItem.appendRow(row)

    def showXulDebugData(self, url):
        self.browser.load(QUrl(url))
        self.statusBar().showMessage(url)
