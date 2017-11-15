#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QTabWidget, QTabBar, QApplication

from XulDebugTool.ui.widget.ConsoleView import ConsoleWindow


class ButtomWindow(QTabWidget):
    def __init__(self, parent=None):
        super(ButtomWindow, self).__init__(parent)
        self.initUi()


    def initUi(self):
        self.tabBar = QTabBar()
        self.consoleView = ConsoleWindow()
        self.tabBar.tabBarClicked.connect(self.status)
        self.tabBar.setExpanding(False)
        self.setTabBar(self.tabBar)
        self.addTab(self.consoleView, "terminal")
        self.consoleView.setVisible(False)
        self.setFixedHeight(30)
        self.setTabPosition(QTabWidget.South)
        self.setStyleSheet(("QTabBar::tab {border: none; height: 30px; width:70px;color:black; padding: 0px;}"
                            "QTabBar::tab:selected { border: none;background: lightgray; } "))

    def status(self):
      if self.tabBar.tabText(self.tabBar.currentIndex()) == 'terminal':
        if self.consoleView.isVisible():
          self.consoleView.setVisible(False)
          self.preHeight = self.width()
          self.setFixedHeight(30)
        else:
          self.consoleView.setVisible(True)
          self.setMaximumHeight(1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ButtomWindow()
    mainWin.show()
    sys.exit(app.exec_())