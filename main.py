'''
Created on 04.Nis.2010

@author: jnmbk
'''

import signal
import sys

from PyQt4 import QtGui

from boxy import Game

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QGraphicsView()
    graphicsScene = Game()
    mainWindow.setScene(graphicsScene)
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
