import random 

from pyrae import dle


TOTALTILES = 100

class TooMuchTilesPut(Exception):
    pass

class EmptyTiles(Exception):
    pass

class MuchTilesPut(Exception):
    pass

class MuchTiles(Exception):
    pass

class TooMuchTiles (Exception):
    pass


class ScrabbleGame:

    def __init__(self, players_count: int):
        self.board = Board()
        self.bag_tiles = BagTiles()
        self.players:list[Player] = []
        for _ in range(players_count):
            self.players.append(Player())
        self.current_player = None
        self.turn = 0

    def next_turn(self):
        if self.current_player == None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            index=self.players.index(self.current_player)+1
            self.current_player=self.players[index]
            
    def distribute_tiles(self):
        for player in self.players:
            player.add_tiles(self.bag_tiles.draw_tiles(7))

    def validate_word(self, word):
        return self.board.validate_word(word)

    def show_board(self):
        return self.board.show_board()

    def show_player_tiles(self):
        return self.current_player.show_tiles()

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
   

class JokerTile(Tile):
    
    def __init__(self, letter, value):
        super().__init__(letter, value)


    def chooseLetter(self,letter_joker):
        for i in DATA:
            if i['letter']==letter_joker.upper():
                self.letter=letter_joker.upper()
                self.value=0
                break
        else:
            raise EmptyTiles 
        
class BagTiles:
    def __init__(self):
        self.tiles=[]
        for i in DATA:
            for j in range(i.get('quantity')):
                self.tiles.append(Tile(i.get("letter"),i.get("value")))
        random.shuffle(self.tiles)
 
    def draw_tiles(self,cantidad):
        tile_drawn=[]
        try:
            if cantidad>len(self.tiles):
                raise TooMuchTiles
            else:
                for i in range(cantidad):
                    tile_drawn.append(self.tiles.pop())
                return tile_drawn
        except TooMuchTiles:
            return tile_drawn


    def put_tiles(self,tiles:list):
        try:
            if len(tiles)+len(self.tiles)<=TOTALTILES:
                self.tiles.extend(tiles)
            else:
                raise TooMuchTilesPut
        except TooMuchTilesPut:
            return TooMuchTilesPut

    def tiles_remaining(self):
        return len(self.tiles)




#tablero
class Board:
    def __init__(self):
        self.grid = [
            [ Cell(None,None,1, '') for _ in range(15) ]
            for _ in range(15)
        ]

    def calculate_word_value(self, word):
        value = 0
        for cell in word:
            value += cell.calculate_value()
        for cell in word:
            if cell.multiplier_type == 'word':
                value *= cell.multiplier
                cell.multiplier = 1
        return value

    
    def validate_word_inside_board(self, word, location, orientation):
        self.word = word
        self.orientation = orientation
        self.position_row = location[0]
        self.position_col = location[1] 
        if orientation == 'H' and len(self.word)<=15-self.position_col:
            return True
        elif orientation == 'V' and len(self.word)<=15-self.position_row:
            return True
        else:
            return False
        
    def empty(self):
        if self.grid[7][7].letter == None:
            self.is_empty = True
        else:
            self.is_empty = False
   
    def validate_word_place_board(self, word, location, orientation):
        valid = self.validate_word_inside_board(word, location, orientation)
        self.empty()
        if self.is_empty == False:
            if valid == True:
                if orientation == "H":
                    for i in self.word:
                        index = self.position_col
                        if self.grid[self.position_row][index].letter is not None:
                            if i != self.grid[self.position_row][index].letter.letter:
                                return False
                        self.position_col += 1
                    return True
                else:
                    for i in self.word:
                        index = self.position_row
                        if self.grid[index][self.position_col].letter is not None:
                            if i != self.grid[index][self.position_col].letter.letter:    
                                return False
                        self.position_row += 1
                    return True
        else:
            if valid == True:
                for i in self.word:
                    if orientation == "H":
                        index = self.position_col
                        if self.position_row == 7 and index == 7:
                            return True
                        self.position_col += 1 
                    else:
                        index = self.position_row
                        if self.position_col == 7 and index == 7:
                            return True
                        self.position_row += 1 
                return False
    
    def validate_word(self, word):

        flag=dle.search_by_word(word)
        if word.lower() not in flag.title:
            return False
        else:
            return True
        
    def show_board(self):
        print('')
        columnas = ['   ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
        print("  ".join(columnas))
        print('-------------------------------------------------')
        filas  = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15']
        for i in range(15):
            print(filas[i], end='|  ')
            for j in range(15):
                if self.grid[i][j].letter is None:
                    print('-', end='  ')
                else:
                    print(self.grid[i][j].letter.letter.upper(), end='  ')
            print('')
        print('')   
    
    

    

class Cell:

    def __init__(self,letter,state,multiplier, multiplier_type):
        self.multiplier = multiplier
        self.multiplier_type = multiplier_type
        self.letter=letter
        self.state=state
        
        
    def add_letter(self, letter:Tile):
        self.letter = letter

    def calculate_value(self):
        if self.letter is None:
            return 0
        if self.multiplier_type == 'letter'and self.state==True:
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

        def change_tiles(self,player_old_tiles_index=[],player_new_tiles=[]):
            tiles_to_change=[]
            for tile_index in range (len(player_old_tiles_index)):
                tiles_to_change.append(self.tiles[player_old_tiles_index[tile_index]-1])
                self.tiles[player_old_tiles_index[tile_index]-1]=player_new_tiles[player_old_tiles_index[tile_index]-1]
            return tiles_to_change
    
        def show_tiles(self):
            return self.tiles