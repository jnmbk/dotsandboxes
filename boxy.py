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

    def get_points(self, box_list):
        #calculate points for given box_list
        #strategy: do not add 3rd sides until all boxes have 2 sides
        points = 0
        for box in box_list:
            if box.enabled_sides() == 4:
                points += 1
            if box.enabled_sides() == 3:
                points -= 1
        return points

    def set_owners(self, box_list, owner):
        #sets owners for unclaimed boxes and returns True if set any boxes
        owned = False
        for box in box_list:
            if box.enabled_sides() == 4 and box.owner == Player.noone:
                box.owner = owner
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
        for line in range(HEIGHT + 1):
            for part in range(HEIGHT):
                self.side_list.append(Side(Orientation.vertical, line, part))
        #horizontal
        for line in range(WIDTH + 1):
            for part in range(WIDTH):
                self.side_list.append(Side(Orientation.horizontal, line, part))
        #create boxes
        self.box_list = []
        for i in range(WIDTH):
            for j in range(HEIGHT):
                sides = self.find_sides(self.side_list, i, j)
                self.box_list.append(Box(sides, i, j))

        #add components to scene
        for side in self.side_list:
            self.addItem(side)
        for box in self.box_list:
            self.addItem(box)
        """
        #now play
        current_player = Player.human
        while self.get_possible_moves(side_list):
            #print "player is %d" % current_player
            #TODO: human starts first, random move
            #computer plays
            #TODO: find max of sum of max value for computer move and min for human next move
            move_list = self.get_possible_moves(side_list)
            side = random.randint(0,len(move_list)-1)
            move_list[side].is_enabled = True
            #print "player draw side: %d" % side
            if not self.set_owners(move_list[side].box_list, current_player):
                #change current_player
                current_player = Player.human if current_player == Player.computer else Player.computer
                print "changed current player to %d, remaining moves: %d" % (current_player, len(move_list))
        human_boxes = 0
        computer_boxes = 0
        for box in box_list:
            if box.owner == Player.human:
                human_boxes += 1
            elif box.owner == Player.computer:
                computer_boxes += 1
        print "human: %d, computer: %d" % (human_boxes, computer_boxes)
        """
    def reset_game(self):
        for side in self.side_list:
            side.reset_enabled()
        for box in self.box_list:
            box.owner = Player.noone
