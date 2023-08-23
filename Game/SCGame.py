

import random


class Tile:

    def __init__(self, letter, value):

        self.letter = letter

        self.value = value

class BagTiles:

    def __init__(self):

        self.tiles = [

            Tile('A', 1),

            Tile('A', 1),

            Tile('A', 1),

            Tile('A', 1),

            Tile('A', 1),

        ]

        random.shuffle(self.tiles)

    def take(self, count):

        tiles = []

        for _ in range(count):

            tiles.append(self.tiles.pop())

        return tiles


    def put(self, tiles):

        self.tiles.extend(tiles)

def seleccionar_fichas(num_fichas):
    return random.sample(fichas, num_fichas)

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

# Conjunto de fichas con letras y valores de puntos

fichas = [
    ("A", 1), ("B", 3), ("C", 3), ("D", 2), ("E", 1), ("F", 4), ("G", 2), ("H", 4),
    ("I", 1), ("J", 8), ("K", 5), ("L", 1), ("M", 3), ("N", 1), ("O", 1), ("P", 3),
    ("Q", 10), ("R", 1), ("S", 1), ("T", 1), ("U", 1), ("V", 4), ("W", 4), ("X", 8),
    ("Y", 4), ("Z", 10)
]
