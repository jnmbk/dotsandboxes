#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from components import *
import random

HEIGHT = 8
WIDTH = 8
LINE_SIZE = 40

class Game(QtGui.QGraphicsScene):
    def find_sides(self, side_list, i, j):
        #return sides for given box
        sides = []
        for side in side_list:
            if side.orientation == Orientation.horizontal and side.line in (i, i+1) and side.part == j:
                sides.append(side)
            if side.orientation == Orientation.vertical and side.line in (j, j+1) and side.part == i:
                sides.append(side)
        return sides

    def get_disabled_sides(self, side_list):
        #returns a list of non enabled sides
        sides = []
        for side in side_list:
            if not side.is_enabled:
                sides.append(side)
        return sides

    def get_possible_moves(self, side_list):
        #return a list of not enabled side indexes
        moves = []
        for side in side_list:
            if not side.is_enabled:
                moves.append(side)
        return moves

    def set_owners(self, box_list, owner):
        #sets owners for unclaimed boxes and returns True if set any boxes
        owned = False
        for box in box_list:
            if box.enabled_sides() == 4 and box.owner == Player.noone:
                box.set_owner(owner)
                owned = True
        return owned

    def undo_move(self, side_list, side):
        side.is_enabled = False
        for box in side.box_list:
            box.owner = Player.noone

    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)
        #create sides
        self.side_list = []
        #vertical
        for line in range(WIDTH + 1):
            for part in range(HEIGHT):
                self.side_list.append(Side(Orientation.vertical, line, part, self))
        #horizontal
        for line in range(HEIGHT + 1):
            for part in range(WIDTH):
                self.side_list.append(Side(Orientation.horizontal, line, part, self))
        #create boxes
        self.box_list = []
        for i in range(WIDTH):
            for j in range(HEIGHT):
                sides = self.find_sides(self.side_list, i, j)
                self.box_list.append(Box(sides, j, i))

        #add components to scene
        for side in self.side_list:
            self.addItem(side)
        for box in self.box_list:
            self.addItem(box)
        #now play
        self.current_player = Player.human

    def reset_game(self):
        for side in self.side_list:
            side.reset_enabled()
        for box in self.box_list:
            box.owner = Player.noone

    def computer_move(self):
        #continue playing until it isn't possible to make a square

        side = self.get_minimax_side()
        side.set_enabled()

        while (self.set_owners(side.box_list, self.current_player)):
            side = self.get_minimax_side()
            side.set_enabled()
        self.current_player = Player.human

    def get_minimax_side(self):
        move_list = self.get_possible_moves(self.side_list)
        random.shuffle(move_list)
        points_list = []
        #calculate_minimax
        for move in move_list:
            point = 0
            for box in move.box_list:
                enabled_sides = box.enabled_sides()
                if enabled_sides == 3:
                    point += 1
                elif enabled_sides == 2:
                    point -= 1
            points_list.append(point)
        sorted_list = []
        sorted_list.extend(points_list)
        sorted_list.sort()
        max_point = sorted_list[-1]

        side = move_list[points_list.index(max_point)]
        return side
