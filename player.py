from base import Figure
from figures import King
from functions import check_dims, check_king_safety, find_king, filter_fields




class Player:

    def __init__(self, color, board):
        self.color = color #kolor gracza
        self.king = find_king(board, color) #referencja na króla
        self.__selected = None #zaznaczona figura
        self.__fields = [] #dostępne pola dla zaznaczonej figury (z uwzględnieniem wszystkich przypadków, np. związania)

    #zaznacza wybraną figurę
    def select(self, fig, board):
        self.__selected = fig
        self.__fields = filter_fields(board, fig, fig.fields(board))
        
    #odznacza zaznaczoną figurę
    def unselect(self):
        self.__selected = None
        self.__fields = []

    #kliknięcie na pole, wyróżnia 4 przypadki // zwraca True jeśli przesunięto figurę (tzn. wykonano pełny ruch) // Argumenty: x, y klikniętego pola, plansza
    def click(self, x, y, board, windowUpdate):
        if check_dims(x, y): #pod warunkiem, że współrzędne są poprawne
            if self.__selected == None:
                if board[y, x] != None and board[y, x].color == self.color:
                    # 1. nie jest zaznaczona żadna figura oraz kliknięto na poprawną figurę gracza
                    self.select(board[y, x], board)
                    return False
                else:
                    # 2. nie jest zaznaczona żadna figura oraz kliknięto na pole puste bądź figurę przeciwnika
                    self.unselect()
                    return False
            else:
                if [y, x] in self.__fields:
                    # 3. jest zaznaczona figura oraz kliknięte pole jest dostępnym polem dla zaznaczonej figury
                    self.__selected.move(x, y, board, windowUpdate)
                    self.unselect()
                    return True
                else:
                    # 4. jest zaznaczona figura ale kliknięte pole jest niedostępne dla zaznaczonej figury
                    self.unselect()
                    return False

