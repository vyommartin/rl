#!/usr/bin/python3

import AI
from board import Board
import csv
import random
import time


class Ur(object):
    """docstring for Ur"""
    AI = 0
    HUMAN = 1

    def __init__(self):
        super(Ur, self).__init__()
        self.board = Board()
        self.players = {
            self.board.p1: {'name': 'Player 1', 'type': self.HUMAN},
            self.board.p2: {'name': 'Player 2', 'type': self.HUMAN}
        }
        self.AI = AI.Player()

    def start(self, options=dict()):
        self.intro(options)
        self.play()

    def intro(self, options=dict()):
        print('###################################')
        print('###### Welcome to Game of UR ######')
        print('###################################')
        print('for rules goto: https://en.wikipedia.org/wiki/Royal_Game_of_Ur')
        print('Watch gameplay: https://www.youtube.com/watch?v=WZskjLq040I')
        inp = 'proceed'
        if not options:
            inp = input('press any key to start or q to quit: ')
        if inp != 'q':
            self.setup(options)

    def setup(self, options=dict()):
        if options:
            gameType = options['gameType']
            autosaveMoves = options['autosaveMoves']
        else:
            print("Choose game type")
            print("1. Player vs Player")
            print("2. Player vs AI")
            print("3. AI vs AI")
            gameType = input("Your choice(1/2/3): ")

            while gameType not in ['1', '2', '3']:
                gameType = input(
                    "Please input choice from (1 or 2 or 3) or q to quit: ")
                if gameType.lower() == 'q':
                    return
            autosaveMoves = input("Autosave moves(y/n)[n]: ")
        self.autosaveMoves = (autosaveMoves.lower() == 'y')
        if gameType is '2':
            self.players[self.board.p2]['type'] = self.AI
        if gameType is '3':
            self.players[self.board.p1]['type'] = self.AI
            self.players[self.board.p2]['type'] = self.AI
        self.gameType = int(gameType)
        self.curPlayer = self.board.p1
        if self.autosaveMoves:
            self.filePointer = open(
                'data/' + str(int(time.time())) + '.csv', 'w+')
            fieldnames = [
                "player",
                "pid",
                "start",
                "step",
                "end",
                "kill",
                "completed",
                "winner"]
            self.dictwriter = csv.DictWriter(
                self.filePointer, fieldnames=fieldnames)
            self.dictwriter.writeheader()

    def play(self):
        completed = False
        winner = None
        quitPieces = [x.lower() + 'q' for x in list(self.players.keys())]
        while (not completed):
            step = self.getDice()
            piece = self.getPlayerPiece(step)
            if piece.lower() in quitPieces:
                break
            if (step == 0) or (piece == "-1"):
                self.board.printer()
                self.switchPlayer(piece)
                continue
            (start, end, kill, pCompleted) = self.board.movePiece(piece, step)
            (completed, winner) = self.board.isCompleted()
            self.saveMove(
                piece,
                start,
                step,
                end,
                kill,
                pCompleted,
                winner)
            self.board.printer()
            self.switchPlayer(piece)

        self.declare(completed, winner)

    def getDice(self):
        return random.randint(0, 4)

    def getPlayerPiece(self, step):
        piece = '-1'
        if step == 0:
            print("No Move for %s  as Dice rolled 0\r\n"
                  % (self.players[self.curPlayer]['name']))
        else:
            pieces = ", ".join(
                self.board.movablePieces(
                    self.curPlayer, step)).replace(
                self.curPlayer, '').split(', ')
            print("Move piece for %s by %s \r\n"
                  % (self.players[self.curPlayer]['name'], str(step)))
            if pieces == ['']:
                print("No more valid moves available.")
                return piece
            print("Please choose a piece from %s \r\n"
                  % (", ".join(pieces)))
            if self.players[self.curPlayer]['type'] == self.AI:
                piece = self.AI.choose(pieces, step, self.board)
            elif self.players[self.curPlayer]['type'] == self.HUMAN:
                piece = input("Your choice (q to quit): ")
                while piece not in pieces:
                    if piece == 'q':
                        break
                    piece = input("Please enter correct choice (q to quit): ")
        return self.curPlayer + piece

    def switchPlayer(self, movedPiece):
        allPlayers = list(self.players.keys())
        allPlayers.remove(self.curPlayer)
        if '-1' not in movedPiece:
            (player, piece, pieces, path) = self.board.idByPiece(movedPiece)
            if self.board.isPieceFinished(movedPiece, path):
                pass
            elif self.board.isPieceDualChance(movedPiece, path):
                return
        self.curPlayer = allPlayers[0]

    def saveMove(self, pid, startPos, step, end, kill, completed, win):
        if self.autosaveMoves is not True:
            return
        self.dictwriter.writerow({
            "player": self.curPlayer,
            "pid": pid,
            "start": startPos,
            "step": step,
            "end": end,
            "kill": kill,
            "completed": completed,
            "winner": win})

    def declare(self, completed, winner):
        if winner is None:
            print("Match abandoned hence no result")
        else:
            print("Winner is %s \r\n" % (self.players[winner]['name']))
            print(''' YIPPIE!!!
              _______
             |       |
            (|       |)
             |       |
              \     /
               `---'
               _|_|_
            ''')
