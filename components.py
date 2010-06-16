#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui
LINE_SIZE=40

class Box(QtGui.QGraphicsRectItem):
    #Four adjacent sides forms a box
    def __init__(self, sides, i, j):
        QtGui.QGraphicsRectItem.__init__(self, i*LINE_SIZE, j*LINE_SIZE, LINE_SIZE, LINE_SIZE)
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.sides = sides
        self.owner = Player.noone
        for side in self.sides:
            side.box_list.append(self)

    def enabled_sides(self):
        enabled_sides = 0
        for side in self.sides:
            enabled_sides += 1 if side.is_enabled else 0
        return enabled_sides

    def set_owner(self, owner):
        self.setBrush(QtGui.QBrush(QtGui.QColor(PlayerColors[owner])))
        self.owner = owner

class Side(QtGui.QGraphicsLineItem):
    def __init__(self, orientation, line, part, game):
        if orientation == Orientation.horizontal:
            x1 = part*LINE_SIZE
            y1 = line*LINE_SIZE
            x2 = (part+1)*LINE_SIZE
            y2 = line*LINE_SIZE
        else:
            x1 = line*LINE_SIZE
            y1 = part*LINE_SIZE
            x2 = line*LINE_SIZE
            y2 = (part+1)*LINE_SIZE
        QtGui.QGraphicsLineItem.__init__(self, x1, y1, x2, y2)
        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor("blue"))
        self.setPen(pen)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setOpacity(0.2)

        self.orientation, self.line, self.part = orientation, line, part
        self.is_enabled = False
        self.game = game
        self.box_list = []

    def hoverEnterEvent(self, event):
        self.setOpacity(1)

    def hoverLeaveEvent(self, event):
        if not self.is_enabled:
            self.setOpacity(0.2)

    def set_enabled(self):
        self.is_enabled = True
        self.setOpacity(1)

    def reset_enabled(self):
        self.is_enabled = False
        self.setOpacity(0.2)

    def mousePressEvent(self, event):
        if not self.is_enabled and self.game.current_player == Player.human:
            self.set_enabled()
            if not self.game.set_owners(self.box_list, self.game.current_player):
                #change current_player
                self.game.current_player = Player.human if self.game.current_player == Player.computer else Player.computer
            if self.game.current_player == Player.computer:
                self.game.computer_move()

class Orientation:
    vertical = 0
    horizontal = 1

class Player:
    human = 0
    computer = 1
    noone = 2

PlayerColors = (
    "blue",
    "red",
)
