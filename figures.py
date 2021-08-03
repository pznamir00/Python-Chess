from base import Figure
from functions import check_dims





class Pawn(Figure):
    def __init__(self, **kwargs):
        super(Pawn, self).__init__(**kwargs)
        self.name = 'pawn'
        self.moved = False #to pole mówi czy figura została ruszona, czy jest to jej pierwszy ruch
        self.hetman = lambda:  Hetman(x=self._coords['x'], y=self._coords['y'], color=self._color) #zwraca hetmana o parametrach identycznych jak self (wywołana w przypadku promocji)
        self.__dir = 1 if self._color == 'black' else -1 #to pole określa kierunek w którym pion się porusza (białe: -1, czarne: 1)

    #nadpisanie settera koordynatów
    @Figure.coords.setter
    def coords(self, ncoords):
        super(Pawn, self.__class__).coords.fset(self, ncoords)
        if not self.moved: #aktualizacja pola moved
            self.moved = True

    def fields(self, board):
        res = []
        x, y = self._coords['x'], self._coords['y']
        if check_dims(x, y+2*self.__dir) and board[y + 2*self.__dir, x] == None and board[y + self.__dir, x] == None and not self.moved:
            res.append([y + 2*self.__dir, x])
        if check_dims(x, y+self.__dir) and board[y + self.__dir, x] == None:
            res.append([y + self.__dir, x])
        if check_dims(x-1, y+self.__dir) and board[y + self.__dir, x - 1] and board[y + self.__dir, x - 1].color != self._color:
            res.append([y + self.__dir, x - 1])
        if check_dims(x+1, y+self.__dir) and board[y + self.__dir, x + 1] and board[y + self.__dir, x + 1].color != self._color:
            res.append([y + self.__dir, x + 1])
        return res





class Bishop(Figure):
    def __init__(self, **kwargs):
        super(Bishop, self).__init__(**kwargs)
        self.name = 'bishop'

    def fields(self, board):
        res = []
        x, y = self._coords['x'], self._coords['y']
        options = [[1,1], [1,-1], [-1,1], [-1,-1]]
        for option in options:
            i = 1
            while check_dims(x+i*option[1], y+i*option[0]) and board[y+i*option[0], x+i*option[1]] == None:
                res.append([y+i*option[0], x+i*option[1]])
                i += 1
            if check_dims(x+i*option[1], y+i*option[0]) and board[y+i*option[0], x+i*option[1]].color != self._color:
                res.append([y+i*option[0], x+i*option[1]])
        return res






class Knight(Figure):
    def __init__(self, **kwargs):
        super(Knight, self).__init__(**kwargs)
        self.name = 'knight'

    def fields(self, board):
        res = []
        x, y = self._coords['x'], self._coords['y']
        options = [[2,1], [2,-1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]]
        for option in options:
            if check_dims(x+option[1], y+option[0]) and (board[y + option[0], x + option[1]] == None or board[y + option[0], x + option[1]].color != self._color):
                res.append([y + option[0], x + option[1]])
        return res




class Rook(Figure):
    def __init__(self, **kwargs):
        super(Rook, self).__init__(**kwargs)
        self.moved = False #mówi czy figura została ruszona
        self.name = 'rook'

    #nadpisanie settera koordynatów
    @Figure.coords.setter
    def coords(self, ncoords):
        super(Rook, self.__class__).coords.fset(self, ncoords)
        if not self.moved: #aktualizuje moved
            self.moved = True

    def fields(self, board):
        res = []
        x, y = self._coords['x'], self._coords['y']
        options = [[0,1], [0,-1], [1,0], [-1,0]]
        for option in options:
            i = 1
            while check_dims(x+i*option[1], y+i*option[0]) and board[y+i*option[0], x+i*option[1]] == None:
                res.append([y+i*option[0], x+i*option[1]])
                i += 1
            if check_dims(x+i*option[1], y+i*option[0]) and board[y+i*option[0], x+i*option[1]].color != self._color:
                res.append([y+i*option[0], x+i*option[1]])
        return res





class Hetman(Figure):
    def __init__(self, **kwargs):
        super(Hetman, self).__init__(**kwargs)
        self.name = 'hetman'

    def fields(self, board):
        f1 = Bishop(x=self._coords['x'], y=self._coords['y'], color=self._color).fields(board)
        f2 = Rook(x=self._coords['x'], y=self._coords['y'], color=self._color).fields(board)
        return f1 + f2





class King(Figure):
    def __init__(self, **kwargs):
        super(King, self).__init__(**kwargs)
        self.moved = False #mówi czy król już został przesunięty
        self.name = 'king'

    @Figure.coords.setter
    def coords(self, ncoords):
        super(King, self.__class__).coords.fset(self, ncoords)
        if not self.moved: #aktualizacja moved
            self.moved = True

    def fields(self, board):
        res = []
        x, y = self._coords['x'], self._coords['y']
        options = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        for option in options:
            if check_dims(x+option[1], y+option[0])  and (board[y + option[0], x + option[1]] == None or board[y + option[0], x + option[1]].color != self._color):
                res.append([y + option[0], x + option[1]])
        
        #jeśli król nie był jeszcze przesunięty, możliwe są również roszady
        if self.moved == False:
            #prawa roszada
            if board[y, x + 1] == None:
                 if board[y, x + 2] == None:
                      if board[y, x + 3] != None and board[y, x + 3].name == 'rook' and board[y, x + 3].moved == False:
                          res.append([y, x + 2])
            #lewa roszada
            if board[y, x - 1] == None:
                if board[y, x - 2] == None:
                     if board[y, x - 3] == None:
                          if board[y, x - 4] != None and board[y, x - 4].name == 'rook' and board[y, x - 4].moved == False:
                              res.append([y, x - 2])
        return res