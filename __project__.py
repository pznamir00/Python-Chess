import numpy as np
from figures import Pawn, Bishop, Rook, Knight, Hetman, King
from functions import filter_fields
from player import Player
from gui import Window
from PyQt5 import QtWidgets





"""
Program szachów
Program jest klasyczną grą w szachy, zawiera gui, systemy wykrywania szachu i mata
Aby wykonać ruch wystarczy kliknąć na figurę a następnie na dostępne dla niej pole
"""





class Chess:

    def __init__(self):
        #domyślna plansza (zawiera symboliczne cyfry, które odpowiadają figurom i w konstruktorze są modyfikowane)
        self.board = np.array([], dtype=object)
        self.__load_board()
        for i, y in enumerate(self.board):
            for j, x in enumerate(y):
                if x == 0: self.board[i, j] = None
                else:
                    c = 'white' if x > 0 else 'black'
                    if np.abs(x) == 1: self.board[i, j] = Pawn(x=j, y=i, color=c)
                    elif np.abs(x) == 2: self.board[i, j] = Bishop(x=j, y=i, color=c)
                    elif np.abs(x) == 3: self.board[i, j] = Knight(x=j, y=i, color=c)
                    elif np.abs(x) == 4: self.board[i, j] = Rook(x=j, y=i, color=c)
                    elif np.abs(x) == 5: self.board[i, j] = Hetman(x=j, y=i, color=c)
                    elif np.abs(x) == 6: self.board[i, j] = King(x=j, y=i, color=c)

        self.__turn = 'white'
        self.__turn_nb = 1
        self.__switch_turn = lambda: 'white' if self.__turn == 'black' else 'black'
        #gui gry
        self.window = Window(self)
        self.__players = {
            'white': Player('white', self.board),
            'black': Player('black', self.board)
        }




    #wczytuje plansze z zewnętrznego pliku board.txt
    def __load_board(self):
        b = [i for i in range(8)]
        with open('board.txt') as text_board:
            for index, line in enumerate(text_board):
                l = [int(i) for i in line.split()]
                b[index] = l
        self.board = np.array(b, dtype=object)
        

    #aktualizacja stanu gry - zmiana tury, sprawdzanie szacha i mata
    def __new_turn(self):
        self.__turn = self.__switch_turn()
        self.__turn_nb += 1
        if self.is_check() == True:
            if self.is_checkmate() == True:
                self.end()
            


    #akcja na kliknięcie pola // Argumenty: x, y klikniętego pola
    def click(self, x, y):
        res = self.__players[self.__turn].click(x, y, self.board, self.window.update)
        if res == True: #jeśli res==True, aktualizuje grę
            self.__new_turn()



    #sprawdza czy nastąpił mat
    def is_checkmate(self):
        for i in self.board:
            for j in i:
                if j != None and j.color == self.__turn:
                    f = filter_fields(self.board, j, j.fields(self.board)) #sprawdza dostępne poprawne pola dla każdej figury gracza
                    if len(f) > 0: #jeśli są dostępne jakiekolwiek pola - nie ma mata
                        return False
        return True


    #sprawdza czy nastąpił szach
    def is_check(self):
        kx, ky = self.__players[self.__turn].king.coords['x'], self.__players[self.__turn].king.coords['y']
        for i in self.board:
            for j in i:
                if j != None and j.color != self.__turn:
                    f = j.fields(self.board) #iteruje figury przeciwnika i ich dostępne pola, jeśli król gracza znajduje się w jakimś - jest szach
                    if [ky, kx] in f:
                        return True
        return False
        
    
                

    #start gry
    def start(self):
        print(self.board)



    #koniec gry
    def end(self):
        self.__turn = self.__switch_turn()
        print('CHECK MATE, WINNER: ', self.__turn)










if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    chess = Chess()
    chess.window.show()
    app.exec()

    
    
