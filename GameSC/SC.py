import random 



class Tile:

    def __init__(self, letter, value):

        self.letter = letter

        self.value = value

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

    def put(self, tiles):
        self.tiles.extend(tiles)
        random.shuffle(self.tiles)

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
            puntuacion += fichas[letra][1] * 2
        elif casillas_usadas[i] == "TL":
            puntuacion += fichas[letra][1] * 3
        elif casillas_usadas[i] == "DW":
            multiplicador *= 2
            puntuacion += fichas[letra][1]
        elif casillas_usadas[i] == "TW":
            multiplicador *= 3
            puntuacion += fichas[letra][1]
        else:
            puntuacion += fichas[letra][1]

    return puntuacion * multiplicador

#tablero
class Board:
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

# Conjunto de fichas con letras y valores de puntos

class Ficha:
    def __init__(self, letra, valor):
        self.letra = letra
        self.valor = valor

fichas = {
    "A": 1, "E": 1, "I": 1, "L": 1, "N": 1, "O": 1, "R": 1, "S": 1, "T": 1, "U": 1,
    "D": 2, "G": 2,
    "B": 3, "C": 3, "M": 3, "P": 3,
    "F": 4, "H": 4, "V": 4, "Y": 4,
    "Ch": 5, "Q": 5,
    "J": 8, "LL": 8, "Ñ": 8, "RR": 8, "X": 8,
    "Z": 10
}

class Player:
    
        def __init__(self):
    
            self.tiles = []
    
        def add_tiles(self, tiles):
    
            self.tiles.extend(tiles)
    
        def remove_tiles(self, tiles):
    
            for tile in tiles:
    
                self.tiles.remove(tile)
    
        def get_tiles(self):
    
            return self.tiles
    
        def get_tiles_letters(self):
    
            return [tile.letter for tile in self.tiles]
    
        def get_tiles_values(self):
    
            return [tile.value for tile in self.tiles]
    
        def get_tiles_values_sum(self):
    
            return sum([tile.value for tile in self.tiles])
    
        def get_tiles_count(self):
    
            return len(self.tiles)
    
        def get_tiles_count_letters(self):
    
            return len(set(self.get_tiles_letters()))
    
        def get_tiles_count_values(self):
    
            return len(set(self.get_tiles_values()))
        