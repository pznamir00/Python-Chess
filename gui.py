from PyQt5 import QtCore, QtGui, QtWidgets
from math import floor
import os



class Window(QtWidgets.QWidget):
    def __init__(self, chess):
        super().__init__()
        self.chess = chess #referencja do sinika
        self.boardFieldDimension = 56
        self.setWindowTitle("Chess game")
        self.setGeometry(300, 300, 800, 800)
        self.figures = {} #grafiki figur (QLabel)
        label = QtWidgets.QLabel(self)
        boardImage = QtGui.QPixmap('graphics/board.png') #grafika planszy
        label.setPixmap(boardImage)
        self.resize(boardImage.width(), boardImage.height())
        self.prepare()
        self.show()

    #kliknięcie na planszę
    def mousePressEvent(self, e):
        #pobieranie koordynatów klikniętego pola
        x = floor(e.x() / self.boardFieldDimension)
        y = floor(e.y() / self.boardFieldDimension)
        self.chess.click(x, y)

    #wczytanie grafik figur na odpowiednie pola
    def prepare(self):
        for i, y in enumerate(self.chess.board):
            for j, x in enumerate(y):
                if x == None: continue
                label = QtWidgets.QLabel(self)
                pre = 'w' if x.color == 'white' else 'b'
                figure = QtGui.QPixmap('graphics/figures/' + pre + x.name + '.png')
                label.setPixmap(figure)
                label.setGeometry(j * self.boardFieldDimension, i * self.boardFieldDimension, self.boardFieldDimension, self.boardFieldDimension)
                self.figures[str(id(x))] = label

    #przesunięcie figury selected
    def update(self, selected, newx, newy):
        x = newx*self.boardFieldDimension
        y = newy*self.boardFieldDimension
        for key, val in self.figures.items():
            if val.x() == x and val.y() == y:
                val.clear()
        self.figures[str(id(selected))].move(x, y)





