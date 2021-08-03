import copy
from scipy.spatial import distance



#sprawdza czy podane koordynaty są poprawne (tzn. czy są w przedziale 0-7) // Argumnety: współrzędne x, y
def check_dims(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8




#znajduje króla gracza o zadanym kolorze // Argumenty: plansza, kolor gracza
def find_king(board, color):
    for i in board:
        for j in i:
            if j != None and j.name == 'king' and j.color == color:
                return j



#filtruje pola funkcją check_king_safety (czyli sprawdza czy ruch na dane pole nie spowoduje mata) // Argumenty: plansza, figura, pola dostępne dla tej figury
def filter_fields(board, figure, fields):
    return [a for a in fields if check_king_safety(board, figure, a[::-1])]




#sprawdza specjalne akcje (roszady i promocje)
def check_special_moves(board, o, px, py, windowUpdate=None):
    if o.name == 'pawn':
        #sprawdzanie promocji
        if (o.color == 'white' and o.coords['y'] == 0) or (o.color == 'black' and o.coords['y'] == 7):
            board[o.coords['y'], o.coords['x']] = o.hetman()
    elif o.name == 'king':
        #sprawdzanie roszad
        d = distance.euclidean([o.coords['x'], o.coords['y']], [px, py])
        if d == 2:
            if o.coords['x'] == 2: #długa roszada
                board[o.coords['y'], 0].move(3, o.coords['y'], board, windowUpdate)
            elif o.coords['x'] == 6: #krótka roszada
                board[o.coords['y'], 7].move(5, o.coords['y'], board, windowUpdate)




#sprawdza czy po danym ruchu nie wystąpi mat // Argumenty: plansza, kolor gracza, [fx, fy] współrzędne figury, którą chcemy przesunąć, [tx, ty] współrzędne docelowe
#ważne: król nie może tu być brany z referencji Player.king, ponieważ jego teoretyczne położenie (jeśli chcemy przesunąć króla) może również ulec zmianie, a ta funkcja bazuje
#na kopii planszy (tzn. jakby ta plansza wyglądała gdyby dana figura poszła w dane miejsce
def check_king_safety(board, figure, nfield):
    king = None
    color = figure.color
    fx = figure.coords['x']
    fy = figure.coords['y']
    tx = nfield[0]
    ty = nfield[1]

    cboard = copy.deepcopy(board) #kopia planszy
    king = find_king(cboard, color)
    cboard[fy, fx].move(tx, ty, cboard) #przesuwa figurę na docelowe pola, ale na kopii planszy (nieoficjalnie)
    for i in cboard:
        for j in i:
            if j != None and j.color != color:
                fields = j.fields(cboard)
                if [king.coords['y'], king.coords['x']] in fields: #jeśli król znajduje się w jakimś polu dostępnym dla przeciwnika, zwróć False
                    return False
    return True