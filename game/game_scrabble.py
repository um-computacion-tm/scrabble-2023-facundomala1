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

class InvalidWordException(Exception):
    pass

class EndTurnException(Exception):
    pass

class EndGameException(Exception):
    pass

class ScrabbleGame:

    def __init__(self, players_count):
        self.board = Board()
        self.tilebag = BagTiles()
        self.players = [Player(number=number) for number in range(players_count)]
        self.current_player = None
        self.round = 1

    def next_turn(self):
        if self.current_player == None:
            self.current_player = self.players[0]
        elif self.current_player == self.players[-1]:
            self.round += 1
            self.current_player = self.players[0]
        else:
            index=self.players.index(self.current_player)+1
            self.current_player=self.players[index]   
    
    def change_tiles(self, old_tiles_index=[]):
        new_tiles=self.tilebag.draw_tiles(len(old_tiles_index))
        old_tiles = []
        for i in old_tiles_index:
            old_tiles.append(self.current_player.tiles[i-1])
            self.current_player.tiles[i-1] = new_tiles.pop(0)
        self.tilebag.put_tiles(old_tiles)
        return old_tiles
    
    def end_game(self):
        if self.tilebag.tiles == []:
            for player in self.players:
                if player.tiles == []:
                    return True
                else:
                    return False
        elif self.players[0].surrender == 3:
            return True
        else:
            return False
   


class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

    def __repr__(self):
        return self.letter
    
 
    
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
 
    def draw_tiles(self,quantity):
        tile_drawn=[]
        try:
            if quantity>len(self.tiles):
                raise TooMuchTiles
            else:
                for i in range(quantity):
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
    
    def shuffle(self):
        random.shuffle(self.tiles)
        return self.tiles
    


#tablero
class Board:
    def __init__(self):
    
        self.grid = [[ Cell(1, '') for _ in range(15) ]for _ in range(15)]
        WORD_MULTIPLIERS = ((0, 0), (7, 0), (0, 7), (7, 7), (0, 14), (7, 14), (14, 0), (14, 7), (14, 14), (1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12), (13, 13), (1, 13), (2, 12), (3, 11), (4, 10), (10, 4), (11, 3), (12, 2), (13, 1))
        LETTER_MULTIPLIERS = ((1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9),(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.validate_multiplier(row, col, WORD_MULTIPLIERS, LETTER_MULTIPLIERS)

    def validate_multiplier(self, row, col, WORD_MULTIPLIERS, LETTER_MULTIPLIERS):
        if (row, col) in LETTER_MULTIPLIERS:
            multiplier=3 if (row, col) in ((1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)) else 2
            self.grid[row][col] = Cell(multiplier, 'letter', '', True)
        elif (row, col) in WORD_MULTIPLIERS:
            multiplier = 3 if (row, col) in ((0, 0), (7, 0), (0, 7), (0, 14), (7, 14), (14, 0), (14, 7), (14, 14)) else 2
            self.grid[row][col] = Cell(multiplier, 'word', '', True)
        else:
            self.grid[row][col] = Cell(1, '', '', False)
    

    def is_empty(self):
        if self.grid[7][7].letter is None:
            return True
    

    def validate_init_of_game(self, word, location, orientation):
        for i in range(len(word)):
            row = location[0] if orientation else location[0] + i
            column = location[1] + i if orientation else location[1]
            if (row, column) == (7, 7):
                return True
        return False
        

    def validate_len_of_word_in_board(self, word, location, orientation):
        location_x = location[0]
        location_y = location[1]
        len_word = len(word)
        if orientation == True:
            if location_x + len_word > 15:
                return False
            else:
                return True
        else:
            if location_y + len_word > 15:
                return False
            else:
                return True

    def validate(self,word,location,orientation):
        exist = self.validate_word(word)
        enter = self.validate_len_of_word_in_board(word,location,orientation)
        is_valid = exist and enter
        if is_valid:
            if self.is_empty():
                return self.validate_init_of_game(word,location,orientation)
            else:
                return self.validate_not_empty(word,location,orientation)
  

    
    
    def validate_word(self, word):

        dle.set_log_level(log_level='CRITICAL')
        flag=dle.search_by_word(word)
        if word.lower() not in flag.title:
            return False
        else:
            return True
        
    def validate_side_cell(self, parameters, cell, index_increment):
        letter, pos, horizontal = parameters[0], parameters[1], parameters[2]
        grid, side_word, index = self.grid, letter, 1
        while cell:
            side_word += cell.letter.lower()
            index += 1
            cell = grid[pos[0]+(index*index_increment)][pos[1]].letter if horizontal else grid[pos[0]][pos[1]+(index*index_increment)].letter
        return side_word

    def check_cells(self, cells, parameters, validators):
        cell, sidecell, invertsidecell = cells[0], cells[1], cells[2]
        letter, pos, horizontal = parameters[0], parameters[1], parameters[2]
        is_valid, intersections = validators[0], validators[1]
        if cell:
            intersections += 1
            is_valid += 1 if cell.letter == letter.upper() else 0
            return [is_valid, intersections]
        elif sidecell and invertsidecell:
            side_word = self.validate_side_cell([letter, pos, horizontal], invertsidecell, -1)[::-1]
            side_word += self.validate_side_cell([letter, pos, horizontal], sidecell, 1)[1:]
        elif sidecell:
            side_word = self.validate_side_cell([letter, pos, horizontal], sidecell, 1)
        elif invertsidecell:
            side_word = self.validate_side_cell([letter, pos, horizontal], invertsidecell, -1)[::-1]
        side_word_is_valid = self.validate_word(side_word)
        if not side_word_is_valid:
            is_valid = -9999
        else:
            is_valid += 1
            intersections += 1
        return [is_valid, intersections]

    def validate_not_empty(self, word, pos, horizontal):
        intersections = 0
        is_valid = 0
        grid = self.grid
        for i in range(len(word)):
            if horizontal:
                cell = grid[pos[0]][pos[1]+i].letter
                sidecell = grid[pos[0] + 1][pos[1] + i].letter
                invertsidecell = grid[pos[0] - 1][pos[1] + i].letter
            else:
                cell = grid[pos[0]+i][pos[1]].letter
                sidecell = grid[pos[0] + i][pos[1] + 1].letter
                invertsidecell = grid[pos[0] + i][pos[1] - 1].letter
            if cell or sidecell or invertsidecell:
                location = (pos[0],pos[1]+i) if horizontal else (pos[0]+i,pos[1])
                checked = self.check_cells([cell, sidecell, invertsidecell], [word[i], location, horizontal], [is_valid, intersections])
                is_valid, intersections = checked[0], checked[1]
        return is_valid != 0 and is_valid == intersections

    def show_board(self):
        view = '       \n     A   B   C   D   E   F   G   H   I   J   K   L   M   N   O  \n'
        for i in range(len(self.grid)):
            view += f'  {i}  ' if i <= 9 else f'  {i} '
            view = self.show_board_wrapper(view,i)
            view += '\n' 
        return view

    def show_board_wrapper(self,view,i):
        for j in range(len(self.grid[i])):
            cell = self.grid[i][j]
            if cell.letter is None:
                if cell.multiplier_type == 'word':
                    view += f'{cell.multiplier}W| '
                elif cell.multiplier_type == 'letter':
                    view += f'{cell.multiplier}L| '
                else:
                    view += '  | '
            elif len(cell.letter.letter) == 2:
                view += f'{cell.letter}| '
            else:
                view += f'{cell.letter} | '
        return view
        
    def put_word(self,word,location,orientation):
        j=0
        for i in range(len(word)):
            cell = self.grid[location[0]][location[1]+i+j] if orientation else self.grid[location[0]+i+j][location[1]]
            while cell.letter:
                j+=1
                cell = self.grid[location[0]][location[1]+i+j] if orientation else self.grid[location[0]+i+j][location[1]]
            cell.letter = word[i]


    def remove_accent(self, word):
        word = word.replace('Á','A')
        word = word.replace('É','E')
        word = word.replace('Í','I')
        word = word.replace('Ó','O')
        word = word.replace('Ú','U')
        return word
    
    def get_word_without_intersections(self,word,location,orientation):
        result = ''
        for i in range(len(word)):
            cell = self.grid[location[0] + (i if not orientation else 0)][location[1] + (i if orientation else 0)].letter
            if not cell:
                result += word[i]
        return result
        
    def calculate_word_value(self, word, location, orientation, first=True):
        word = Player().split_word(word)
        points = 0
        word_multiplier = 1
        i = 0
        for letter in word:
            cell, invert_cell, side_cell = self.get_cells(location, i, orientation)
            available = not cell.letter and first
            j = 1
            if invert_cell and invert_cell.letter and available:
                side_word, j = self.get_side_word(invert_cell, i, (orientation,True), location, letter)
                points += self.calculate_word_value(side_word, (location[0] - j + 1, location[1] + i) if orientation else (location[0] + i, location[1] - j + 1), not orientation, False)
            elif side_cell and side_cell.letter and available:
                side_word, j = self.get_side_word(side_cell, i, (orientation,False), location, letter)
                points += self.calculate_word_value(side_word, (location[0], location[1] + i) if orientation else (location[0] + i, location[1]), not orientation, False)
            letter_value = self.get_letter_value(letter)
            word_multiplier, points = self.update_multipliers(cell, letter_value, word_multiplier, points, first)
            i += 1
        points = points * word_multiplier
        return points        
    
    def get_cells(self, location, i, orientation):
        cell = self.grid[location[0] + (i if not orientation else 0)][location[1] + (i if orientation else 0)]
        invert_cell = self.grid[location[0] - i][location[1] - i] if not orientation and location[0] - i >= 0 and location[1] - i >= 0 else None
        side_cell = self.grid[location[0] - i][location[1] + i] if orientation and location[0] - i >= 0 and location[1] + i < 15 else None
        return cell, invert_cell, side_cell
    
    def get_side_word(self, cell, i, orientation, location, letter):
        word = ''
        j = 0
        while cell.tile:
            word += cell.tile.letter
            j += 1
            cell = self.grid[location[0] - j + 1][location[1] + i] if orientation[0] else self.grid[location[0] + i][location[1] - j + 1]
        word += letter
        return word, j
    
    def get_letter_value(self, letter):
        for tile in DATA:
            if letter == tile['letter']:
                return tile['value']
            
    def update_multipliers(self, cell, letter_value, word_multiplier, points, first):
        if cell.multiplier_type == 'letter':
            points += letter_value * cell.multiplier
        elif cell.multiplier_type == 'word':
            word_multiplier *= cell.multiplier
            points += letter_value
        else:
            points += letter_value
        return word_multiplier, points
    
    

    

class Cell:

    def __init__(self, multiplier, multiplier_type='',letter=None,active=True):
        self.multiplier = multiplier
        self.multiplier_type = multiplier_type
        self.letter=None
        self.active = True

        
    def add_letter(self, tile):
        self.letter = tile


    def calculate_value(self):
        if self.letter is None:
            return 0
        if self.multiplier_type == 'letter'and self.state==True:
            return self.letter.value * self.multiplier
        else:
            return self.letter.value
    
    
    
class Player:
    
    def __init__(self,name='',number=0,score=0,bag_tiles=None):
        self.name = name
        self.number = number
        self.score = score
        self.tiles = []
        self.surrender = 0


    def add_tiles(self,tiles):
        self.tiles.extend(tiles)
    
    def show_tiles(self):
        tiles=[]
        for tile in self.tiles:
            tiles.append(tile.letter)
        return tiles
    
    def take_tiles(self,word):
        word = self.split_word(word)
        tiles=[]
        for letter in word:
            for tile in self.tiles:
                if tile.letter==letter.upper():
                    tiles.append(tile)
                    self.tiles.remove(tile)
                    break
        return tiles
        
    def has_tiles(self,word):
        lectern = self.tiles.copy()
        cont=0
        word = self.split_word(word)
        for letter in word:
            for tile in lectern:
                if tile.letter == letter.upper():
                    lectern.remove(tile)
                    cont+=1
                    break
        if cont == len(word):
            return True
        else:
            return False

    
    def split_word(self,word):
        word = word.upper()
        if 'CH' in word:
            word = word.replace('CH','1')
        if 'LL' in word:
            word = word.replace('LL','2')
        if 'RR' in word:
            word = word.replace('RR','3')
        result = []
        for letter in word:
            if letter == '1':
                result.append('CH')
            elif letter == '2':
                result.append('LL')
            elif letter == '3':
                result.append('RR')
            else:
                result.append(letter)
        return result

