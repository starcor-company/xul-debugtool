import pyperclip
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QMenu, QAction

from XulDebugTool.ui.widget.DataQueryDialog import DataQueryDialog
from XulDebugTool.ui.widget.model.FavoriteDB import FavoriteDB
from XulDebugTool.utils.IconTool import IconTool

ROOT_PROVIDERQUERYHISTORY = "history"
ROOT_FAVORITES = "favorites"

ITEM_TYPE_FAVORITES = 'favorites_type'
ITEM_TYPE_HISTORY = 'history_type'
ITEM_TYPE_URL = 'url_type'

class FavoriteTreeView(QTreeView):
    def __init__(self,window, parent=None):
        self.mainWindow = window
        try:
            super(FavoriteTreeView,self).__init__(parent)
            self.favoriteDB = FavoriteDB()
            self.treeModel = QStandardItemModel()
            self.favorites = QStandardItem(ROOT_FAVORITES)
            self.buildFavoritesTree()
            self.providerQueryHistory = QStandardItem(ROOT_PROVIDERQUERYHISTORY)
            self.buildQueryHistory()
            self.treeModel.appendColumn([self.favorites,self.providerQueryHistory])
            self.treeModel.setHeaderData(0, Qt.Horizontal, 'record')

            self.setModel(self.treeModel)
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.openContextMenu)
            self.doubleClicked.connect(self.onTreeItemDoubleClicked)
            # self.clicked.connect(self.clickState)
        except Exception as e:
            print(e)

    def buildFavoritesTree(self):
        self.favorites.removeRows(0,self.favorites.rowCount())
        rows = self.favoriteDB.selectFavorites("favorite = 1")
        for i,row in enumerate(rows):
            providerItem = QStandardItem(row[1] + "   " + row[3])
            providerItem.type = ITEM_TYPE_FAVORITES
            providerItem.id = row[0]
            providerItem.name = row[1]
            providerItem.url = row[2]
            providerItem.date = row[3]
            providerItem.favorite = row[4]
            urlItem = QStandardItem(row[2])
            urlItem.type = ITEM_TYPE_URL
            providerItem.appendRow(urlItem)
            self.favorites.appendRow(providerItem)

    def buildQueryHistory(self):
        self.providerQueryHistory.removeRows(0,self.providerQueryHistory.rowCount())
        rows = self.favoriteDB.selectFavorites()
        for i,row in enumerate(rows):
            providerItem = QStandardItem(row[1]+"   "+row[3])
            providerItem.type = ITEM_TYPE_HISTORY
            providerItem.id = row[0]
            providerItem.name = row[1]
            providerItem.url = row[2]
            providerItem.date = row[3]
            providerItem.favorite = row[4]
            urlItem = QStandardItem(row[2])
            urlItem.type = ITEM_TYPE_URL
            providerItem.appendRow(urlItem)
            self.providerQueryHistory.appendRow(providerItem)


    @pyqtSlot(QModelIndex)
    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if item.type == ITEM_TYPE_FAVORITES or item.type == ITEM_TYPE_HISTORY:
            self.showQueryDialog(item)

    @pyqtSlot(QPoint)
    def openContextMenu(self, point):
        index = self.indexAt(point)
        if not index.isValid():
            return
        item = self.treeModel.itemFromIndex(index)
        menu = QMenu()

        if item.type == ITEM_TYPE_HISTORY:
            queryAction = QAction(IconTool.buildQIcon('data.png'), 'Query Data...', self,triggered=lambda: self.showQueryDialog(item))
            queryAction.setShortcut('Alt+Q')
            menu.addAction(queryAction)

            favoritesAction = QAction(IconTool.buildQIcon('favorites_64.png'),'add to favorites',self,triggered = lambda: self.add2Favorites(item))
            favoritesAction.setShortcut('Alt+F')
            menu.addAction(favoritesAction)

            deleteAction = QAction(IconTool.buildQIcon('clear.png'),'delete item',self,triggered = lambda: self.deleteFavorite(item))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        if item.type == ITEM_TYPE_FAVORITES:
            queryAction = QAction(IconTool.buildQIcon('data.png'), 'Query Data...', self,triggered=lambda: self.showQueryDialog(item))
            queryAction.setShortcut('Alt+Q')
            menu.addAction(queryAction)

            disFavoritesAction = QAction(IconTool.buildQIcon('favorites_64.png'), 'remove to favorites', self,triggered=lambda: self.remove2Favorites(item))
            disFavoritesAction.setShortcut('Alt+F')
            menu.addAction(disFavoritesAction)

            deleteAction = QAction(IconTool.buildQIcon('clear.png'), 'delete item', self,triggered=lambda: self.deleteFavorite(item))
            deleteAction.setShortcut('Ctrl+D')
            menu.addAction(deleteAction)

        if item.type == ITEM_TYPE_URL:
            copyAction = QAction(IconTool.buildQIcon('copy.png'), 'Copy', self,triggered=lambda: pyperclip.copy('%s' % index.data()))
            copyAction.setShortcut('Ctrl+C')
            menu.addAction(copyAction)

        menu.exec_(self.viewport().mapToGlobal(point))


    def showQueryDialog(self,item):
        self.dialog = DataQueryDialog(item)
        self.dialog.finishSignal.connect(self.mainWindow.onGetQueryUrl)
        self.dialog.show()

    def add2Favorites(self,item):
        self.favoriteDB.updateFavorites(item.id, favorite='1')
        self.updateTree()

    def deleteFavorite(self,item):
        sentance = "id = " + str(item.id)
        self.favoriteDB.deleteFavorites(sentance)
        self.updateTree()

    def remove2Favorites(self,item):
        self.favoriteDB.updateFavorites(item.id, favorite='0')
        self.updateTree()

    def updateTree(self):
        self.buildFavoritesTree()
        self.buildQueryHistory()



