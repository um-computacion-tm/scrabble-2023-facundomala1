import random 

TOTALTILES = 100

class MuchTilesPut(Exception):
    pass

class MuchTiles(Exception):
    pass

class ScrabbleGame:

    def __init__(self, players_count):

        self.players = []
        self.bag_tiles = BagTiles(fichas_disponibles)
        self.current_player = None
        self.board = Board()
        for number in range(players_count):
            self.players.append(Player(number=number))

    def start_game(self):
            
            for player in self.players:
                player.add_tiles(self.bag_tiles.take(7))
            self.current_player = self.players[0]   
    
    #revisar

    def draw_game(self,cantidad):
        tile_drawn=[]
        try:
            if cantidad>len(self.tiles):
                raise MuchTiles
            else:
                for i in range(cantidad):
                    tile_drawn.append(self.tiles.pop())
                return tile_drawn
        except MuchTiles:
            return tile_drawn

    def next_turn(self):
        if self.current_player == None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            index=self.players.index(self.current_player)+1
            self.current_player=self.players[index]


    def validate_word(self, word):
        if word in self.words:
            return True
        else:
            return False

    def end_game(self):

        if  self.bag_tiles == []:
            return True
        else:
            return False
        
        


class Tile:

    def __init__(self, letter, value):

        self.letter = letter
        self.value = value
    
    DATA= [
    {"letter": "A", "value": 1, "quantity": 12},
    {"letter": "B", "value": 3, "quantity": 2},
    {"letter": "C", "value": 3, "quantity": 4},
    {"letter": "D", "value": 2, "quantity": 5},
    {"letter": "E", "value": 1, "quantity": 12},
    {"letter": "F", "value": 4, "quantity": 1},
    {"letter": "G", "value": 2, "quantity": 2},
    {"letter": "H", "value": 4, "quantity": 2},
    {"letter": "I", "value": 1, "quantity": 6},
    {"letter": "J", "value": 8, "quantity": 1},
    {"letter": "L", "value": 1, "quantity": 4},
    {"letter": "M", "value": 3, "quantity": 2},
    {"letter": "N", "value": 1, "quantity": 5},
    {"letter": "Ñ", "value": 8, "quantity": 1},
    {"letter": "O", "value": 1, "quantity": 9},
    {"letter": "P", "value": 3, "quantity": 2},
    {"letter": "Q", "value": 5, "quantity": 1},
    {"letter": "R", "value": 1, "quantity": 5},
    {"letter": "S", "value": 1, "quantity": 6},
    {"letter": "T", "value": 1, "quantity": 4},
    {"letter": "U", "value": 1, "quantity": 5},
    {"letter": "V", "value": 4, "quantity": 1},
    {"letter": "X", "value": 8, "quantity": 1},
    {"letter": "Y", "value": 4, "quantity": 1},
    {"letter": "Z", "value": 10, "quantity": 1},
    {"letter": "CH", "value": 5, "quantity": 1},
    {"letter": "LL", "value": 8, "quantity": 1},
    {"letter": "RR", "value": 8, "quantity": 1},
    {"letter": "_", "value": 0, "quantity": 2} ]


class BagTiles:
    def __init__(self, fichas):
        self.tiles = list(fichas)
        random.shuffle(self.tiles)

    def take(self, count):
        if count > len(self.tiles):
            return None                     # No hay suficientes fichas en la bolsa
        taken_tiles = random.sample(self.tiles, count)
        for tile in taken_tiles:
            self.tiles.remove(tile)
        return taken_tiles

#revisar
    def put_tiles(self, tiles:list):
        self.tiles.extend(tiles)
        random.shuffle(self.tiles)
        try:
            if len(tiles)+len(self.tiles)<=TOTALTILES:
                    self.tiles.extend(tiles)
            else:
                    raise MuchTilesPut
        except MuchTilesPut:
                return MuchTilesPut


# Definición de las fichas disponibles
fichas_disponibles = [
    Tile('A', 1),
    Tile('A', 1),
    Tile('A', 1),
    Tile('A', 1),
    Tile('A', 1),
    #(otras fichas con sus letras y valores)
]

# Crear una instancia de BagTiles con las fichas disponibles
bag = BagTiles(fichas_disponibles)

# Definir la función de selección de fichas
def seleccionar_fichas(num_fichas):
    return bag.take(num_fichas)

# Función para calcular la puntuación de una palabra
def calcular_puntuacion(palabra, casillas_usadas):
    puntuacion = 0
    multiplicador = 1

    for i, letra in enumerate(palabra):
        if casillas_usadas[i] == "DL":
            puntuacion += Tile[letra][1] * 2
        elif casillas_usadas[i] == "TL":
            puntuacion += Tile[letra][1] * 3
        elif casillas_usadas[i] == "DW":
            multiplicador *= 2
            puntuacion += Tile[letra][1]
        elif casillas_usadas[i] == "TW":
            multiplicador *= 3
            puntuacion += Tile[letra][1]
        else:
            puntuacion += Tile[letra][1]

    return puntuacion * multiplicador

#tablero
class Board:
    def __init__(self,grid=None):
        self.grid = [[ Cell(1, '') for _ in range(15) ]for _ in range(15)]
        self.grid[7][7].multiplier_type = 'word'
        self.grid[7][7].multiplier = 3
        self.grid[0][0].multiplier_type = 'word'
        self.grid[0][0].multiplier = 3
        self.grid[0][7].multiplier_type = 'word'

    def calculate_word_value(self, word):
        value = 0
        for cell in word:
            value += cell.calculate_value()
        for cell in word:
            if cell.multiplier_type == 'word':
                value *= cell.multiplier
                cell.multiplier = 1
        return value
    
    def validate_len_of_word_in_board(self, word, location, orientation):
        location_x = location[0]
        location_y = location[1]
        len_word = len(word)
        if orientation == 'H':
            if location_x + len_word > 15:
                return False
            else:
                return True
        else:
            if location_y + len_word > 15:
                return False
            else:
                return True

    def put_word(self,word,location, orientation):
        location_x = location[0]
        location_y = location[1]
        if orientation == 'V':
            for i in range(len(word)):
                self.grid[location_x+i][location_y].add_letter(word[i])
        else:
            for i in range(len(word)):
                self.grid[location_x][location_y+i].add_letter(word[i])

    def is_empty(self):
        if self.grid[7][7].letter is None:
            return True


    tablero = [
        ["TW", "", "", "DL", "", "", "", "TW", "", "", "", "DL", "", "", "TW"],
        ["", "DW", "", "", "", "TL", "", "", "", "TL", "", "", "", "DW", ""],
        ["", "", "DW", "", "", "", "DL", "", "DL", "", "", "", "DW", "", ""],
        ["DL", "", "", "DW", "", "", "", "DL", "", "", "", "DW", "", "", "DL"],
        ["", "", "", "", "DW", "", "", "", "", "", "DW", "", "", "", ""],
        ["", "TL", "", "", "", "TL", "", "", "", "TL", "", "", "", "TL", ""],
        ["", "", "DL", "", "", "", "DL", "", "DL", "", "", "", "DL", "", ""],
        ["TW", "", "", "DL", "", "", "", "S", "", "", "", "DL", "", "", "TW"],
        ["", "", "DL", "", "", "", "DL", "", "DL", "", "", "", "DL", "", ""],
        ["", "TL", "", "", "", "TL", "", "", "", "TL", "", "", "", "TL", ""],
        ["", "", "", "", "DW", "", "", "", "", "", "DW", "", "", "", ""],
        ["DL", "", "", "DW", "", "", "", "DL", "", "", "", "DW", "", "", "DL"],
        ["", "", "DW", "", "", "", "DL", "", "DL", "", "", "", "DW", "", ""],
        ["", "DW", "", "", "", "TL", "", "", "", "TL", "", "", "", "DW", ""],
        ["TW", "", "", "DL", "", "", "", "TW", "", "", "", "DL", "", "", "TW"]
    ]

    

class Cell:

    def __init__(self, multiplier, multiplier_type):

        self.multiplier = multiplier

        self.multiplier_type = multiplier_type

        self.letter = None


    def add_letter(self, letter:Tile):

        self.letter = letter


    def calculate_value(self):

        if self.letter is None:

            return 0

        if self.multiplier_type == 'letter':

            return self.letter.value * self.multiplier

        else:

            return self.letter.value


class Player:
    
        def __init__(self,name="",number=0,score=0,bag_tiles=0):
            self.name = name
            self.score = score
            self.bag_tiles = bag_tiles
            self.number = number
            self.tiles = []

        
        def add_tiles(self,tiles):
            self.tiles.extend(tiles)

        def remove_tiles(self,tiles):
            for tile in tiles:
                self.tiles.remove(tile)
        
        def change_tiles(self,player_old=[],player_new=[]):
            tiles_to_change = []
            for tile in player_old:
                self.tiles.remove(tile)
                tiles_to_change.append(tile)
            for tile in player_new:
                self.tiles.append(tile)
                tiles_to_change.remove(tile)
            return tiles_to_change
    
