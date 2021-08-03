import abc
from functions import check_special_moves



#klasa bazowa dla figur
class Figure:
    def __init__(self, **kwargs):
        self.name = '' #nazwa figury (w celu łatwiejszego i szybszego identyfikowania rodzaju figury), np. "king", "pawn" itd.
        self._coords = { #koordynaty
            'x': kwargs['x'],
            'y': kwargs['y']    
        }
        self._color = kwargs['color'] #kolor figury

    #zwraca dostępne pola dla danej figury (np. goniec pola po skosie, skoczek pola w kombinacje litery L idt.)
    @abc.abstractmethod
    def fields(self, board):
        pass

    #zwraca koordynaty
    @property
    def coords(self):
        return self._coords

    #ustawia koordynaty
    @coords.setter
    def coords(self, ncoords):
        self._coords = {
            'x': ncoords[0],
            'y': ncoords[1]
        }
    
    #zwraca kolor
    @property
    def color(self):
        return self._color

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    #przesuwanie self figury na pola x, y
    def move(self, x, y, board, windowUpdate=None):
        board[self._coords['y'], self._coords['x']] = None
        board[y, x] = self
        px, py = self._coords['x'], self._coords['y']
        self.coords = [x, y]
        check_special_moves(board, self, px, py, windowUpdate) #specialne ruchy (np. roszada)
        if windowUpdate: windowUpdate(self, x, y) #aktualizacja graficzna figury (referencja do metody update w klasie Window)





