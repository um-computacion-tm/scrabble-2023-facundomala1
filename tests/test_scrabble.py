
import unittest
from unittest.mock import patch
from game.game_scrabble import *


class TestInitialization(unittest.TestCase):
    def test_init(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertIsNotNone(scrabble_game.board)
        self.assertEqual(len(scrabble_game.players), 3)
        self.assertIsNotNone(scrabble_game.tilebag)

    def test_next_turn_when_game_is_starting(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.next_turn()
        self.assertEqual (scrabble_game.current_player , scrabble_game.players[0])

    def test_next_turn_when_player_is_not_the_first(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        scrabble_game.next_turn()
        self.assertEqual (scrabble_game.current_player , scrabble_game.players[1])

    def test_next_turn_when_player_is_last(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.next_turn()
        self.assertEqual (scrabble_game.current_player, scrabble_game.players[0])
        
    @patch('game.BagTiles.draw_tiles')
    def test_change_tiles(self, mock_take_tiles):
        scrabble = ScrabbleGame(2)
        initial_value = len(scrabble.tilebag.tiles)
        scrabble.current_player = scrabble.players[0]
        tileA = Tile('A',1)
        tileE = Tile('A',1)
        tileF = Tile('F',1)
        scrabble.players[0].tiles = [tileA,tileE,tileE,tileA,tileA,tileA,tileA]
        mock_take_tiles.return_value = [tileF,tileF]
        scrabble.change_tiles((2,3))
        expected = [tileA,tileF,tileF,tileA,tileA,tileA,tileA]
        self.assertEqual(scrabble.players[0].tiles, expected)
        self.assertEqual(len(scrabble.tilebag.tiles), initial_value)

    def test_end_game(self):
        scrabble = ScrabbleGame(2)
        scrabble.current_player = scrabble.players[0]
        scrabble.current_player.surrender = 3
        self.assertEqual(scrabble.end_game(), True)

    def test_end_game_if_tilebag_is_empty(self):
        scrabble = ScrabbleGame(2)
        scrabble.current_player = scrabble.players[0]
        scrabble.tilebag.tiles = []
        self.assertEqual(scrabble.end_game(), True)
    
    def test_end_game_false(self):
        scrabble = ScrabbleGame(2)
        scrabble.current_player = scrabble.players[0]
        scrabble.tilebag.tiles = []
        scrabble.current_player.tiles = [Tile('A',1)]
        self.assertEqual(scrabble.end_game(), False)

    def test_end_game_false_2(self):
        scrabble = ScrabbleGame(2)
        scrabble.current_player = scrabble.players[0]
        scrabble.tilebag.tiles = [Tile('A',1)]
        scrabble.current_player.tiles = [Tile('A',1)]
        self.assertEqual(scrabble.end_game(), False)



class TestTiles(unittest.TestCase):

    def test_tile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)


class TestJoker(unittest.TestCase):

    def test_Joker(self):
        tilebag=BagTiles()
        tilebag.draw_tiles(7)
        tilebag.put_tiles([JokerTile('A',1)])
        self.assertEqual(tilebag.tiles_remaining(),TOTALTILES-6)

    def test_Joker_chooseLetter(self):
        jokertile = JokerTile('_', 0)
        jokertile.chooseLetter('a')
        self.assertEqual(jokertile.letter, 'A')
        self.assertEqual(jokertile.value, 0)

    def test_Joker_chooseLetter_without_letters(self):
        joker_tile=JokerTile('_',0)
        with self.assertRaises(EmptyTiles):
            joker_tile.chooseLetter('w')


class TestTileBag(unittest.TestCase):

    def test_tile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)

    def test_repr(self):
        tile = Tile('A', 1)
        self.assertEqual(repr(tile), 'A')


class TestJoker(unittest.TestCase):

    def test_Joker(self):
        tilebag=BagTiles()
        tilebag.draw_tiles(7)
        tilebag.put_tiles([JokerTile('A',1)])
        self.assertEqual(tilebag.tiles_remaining(),TOTALTILES-6)

    def test_Joker_chooseLetter(self):
        jokertile = JokerTile('_', 0)
        jokertile.chooseLetter('a')
        self.assertEqual(jokertile.letter, 'A')
        self.assertEqual(jokertile.value, 0)

    def test_Joker_chooseLetter_without_letters(self):
        joker_tile=JokerTile('_',0)
        with self.assertRaises(EmptyTiles):
            joker_tile.chooseLetter('w')


class TestBagTiles(unittest.TestCase):

    def test_tilebag(self):
        tilebag = BagTiles()
        self.assertEqual(tilebag.tiles_remaining(), TOTALTILES)

    def test_draw_tiles(self):
        tilebag = BagTiles()
        tilebag.draw_tiles(7)
        self.assertEqual(tilebag.tiles_remaining(), TOTALTILES-7)
        
    def test_draw_too_much_tiles(self):
        tilebag= BagTiles()
        self.assertEqual(tilebag.draw_tiles(TOTALTILES+1),[])
        
    def test_put_tiles(self):
        tilebag=BagTiles()
        taken=tilebag.draw_tiles(6)
        tilebag.put_tiles([taken[0], taken[5], taken[2]])
        self.assertEqual(tilebag.tiles_remaining(),TOTALTILES-3)

    def test_put_too_much_tiles(self):
        tilebag=BagTiles()
        tilebag.put_tiles([Tile('A',1)])
        self.assertEqual(tilebag.tiles_remaining(),TOTALTILES)
        
    def test_shuffle(self):
        tilebag=BagTiles()
        tilebag.shuffle()
        self.assertEqual(tilebag.tiles_remaining(),TOTALTILES)
class TestPlayer(unittest.TestCase):
    def test_init(self):
        player=Player('Fernando',0,0,BagTiles())
        self.assertEqual(player.name,'Fernando')
        self.assertEqual(player.score,0)
        self.assertEqual(player.number,0)
        self.assertEqual(len(player.tiles),0)
    
    def test_add_tiles(self):
        player=Player('Fernando',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1)]
        player.add_tiles(tiles)
        self.assertEqual(len(player.tiles),3)
        self.assertEqual(player.tiles[0].letter,'A')
        self.assertEqual(player.tiles[1].letter,'B')
        self.assertEqual(player.tiles[2].letter,'C')

    def test_show_tiles(self):
        player=Player('Fernando',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1)]
        player.add_tiles(tiles)
        self.assertEqual(player.show_tiles(),['A','B','C'])

    def test_take_tiles(self):
        player=Player('Fernando',0,0,BagTiles())
        tileA = Tile('A',1)
        tileB = Tile('B',1)
        tileC = Tile('C',1)
        tiles=[tileA,tileB,tileC]
        player.add_tiles(tiles)
        self.assertEqual(player.take_tiles('AB'),[tileA,tileB])
        self.assertEqual(player.tiles,[tileC])

    def test_has_tiles(self):
        player=Player('Fernando',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1)]
        player.add_tiles(tiles)
        self.assertTrue(player.has_tiles('ABC'))

    def test_not_has_tiles(self):
        player=Player('Fernando',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1),Tile('S',2)]
        player.add_tiles(tiles)
        self.assertFalse(player.has_tiles('CASA'))

    def test_split_word(self):
        player = Player('Fernando',0,0,BagTiles())
        self.assertEqual(player.split_word('CH'),['CH'])
        self.assertEqual(player.split_word('LL'),['LL'])
        self.assertEqual(player.split_word('RR'),['RR'])
        self.assertEqual(player.split_word('CHLLRR'),['CH','LL','RR'])
     

class TestBoard(unittest.TestCase):
    def test_init(self):
        board = Board()            
        self.assertEqual(len(board.grid),15,)
        self.assertEqual(len(board.grid[0]),15,)   

    def test_is_empty(self):
        board = Board()
        self.assertEqual(board.is_empty(), True)

    def test_not_empty(self):
        board = Board()
        board.grid[7][7].letter = Tile('c',1)
        board.grid[7][8].letter = Tile('a',1)
        board.grid[7][9].letter = Tile('s',2)
        board.grid[7][10].letter = Tile('a',1)
        self.assertEqual(board.is_empty(), False)

    def test_len_of_word_in_board_x(self):
        board = Board()
        word = 'facultad'
        location = (5,4)
        orientation = True
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),True)

    def test_len_of_word_in_board_y(self):
        board = Board()
        word = 'facultad'
        location = (5,4)
        orientation = False
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),True)

    def test_len_of_word_out_of_board_x(self):
        board = Board()
        word = 'facultad'
        location = (10,5)
        orientation = True
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),False)

    def test_len_of_word_out_of_board_y(self):
        board = Board()
        word = 'facultad'
        location = (5,10)
        orientation = False
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),False)

    def test_validate_word_in_board_orientation(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,4)
        orientation = True
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)

    def test_validate_word_in_board_vertical(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (4,7)
        orientation = False
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)

    def test_not_validate_word_in_board_orientation(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (5,8)
        orientation = True
        self.assertEqual(board.validate_init_of_game(word,location,orientation),False)

    def test_not_validate_word_in_board_vertical(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (8,5)
        orientation = False
        self.assertEqual(board.validate_init_of_game(word,location,orientation),False)

    def test_not_empty(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (6,7)
        orientation = False
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)
        

    def test_show_board(self):
        board = Board()
        result = board.show_board()
        expected = '''       
     A   B   C   D   E   F   G   H   I   J   K   L   M   N   O  
  0  3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
  1    | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  2    |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  3  2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  4    |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  5    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  6    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  7  3W|   |   | 2L|   |   |   | 2W|   |   |   | 2L|   |   | 3W| 
  8    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  9    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  10   |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  11 2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  12   |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  13   | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  14 3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
'''
        self.maxDiff = None
        self.assertEqual(result, expected)
    
    def test_show_board_with_word(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',1)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',2)
        board.grid[7][10].letter = Tile('A',1)
        result = board.show_board()
        expected = '''       
     A   B   C   D   E   F   G   H   I   J   K   L   M   N   O  
  0  3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
  1    | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  2    |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  3  2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  4    |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  5    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  6    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  7  3W|   |   | 2L|   |   |   | C | A | S | A | 2L|   |   | 3W| 
  8    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  9    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  10   |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  11 2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  12   |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  13   | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  14 3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
'''
        self.maxDiff = None
        self.assertEqual(result, expected)

    def test_show_board_with_word_2(self):
        board = Board()
        board.grid[7][7].letter = Tile('CH',5)
        board.grid[7][8].letter = Tile('O',1)
        board.grid[7][9].letter = Tile('Z',1)
        board.grid[7][10].letter = Tile('A',1)
        result = board.show_board()
        expected = '''       
     A   B   C   D   E   F   G   H   I   J   K   L   M   N   O  
  0  3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
  1    | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  2    |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  3  2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  4    |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  5    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  6    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  7  3W|   |   | 2L|   |   |   | CH| O | Z | A | 2L|   |   | 3W| 
  8    |   | 2L|   |   |   | 2L|   | 2L|   |   |   | 2L|   |   | 
  9    | 3L|   |   |   | 3L|   |   |   | 3L|   |   |   | 3L|   | 
  10   |   |   |   | 2W|   |   |   |   |   | 2W|   |   |   |   | 
  11 2L|   |   | 2W|   |   |   | 2L|   |   |   | 2W|   |   | 2L| 
  12   |   | 2W|   |   |   | 2L|   | 2L|   |   |   | 2W|   |   | 
  13   | 2W|   |   |   | 3L|   |   |   | 3L|   |   |   | 2W|   | 
  14 3W|   |   | 2L|   |   |   | 3W|   |   |   | 2L|   |   | 3W| 
'''
        self.maxDiff = None
        self.assertEqual(result, expected)

    def test_show_overlapping_words(self):
        board = Board()
        board.grid[7][7].letter = Tile('c',1)
        board.grid[7][8].letter = Tile('a',1)
        board.grid[7][9].letter = Tile('s',2)
        board.grid[7][10].letter = Tile('a',1)
        word = [Tile('s',2),Tile('a',1),Tile('c',1),Tile('a',1)]
        location = (7,7)
        orientation = True
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)

    @patch('game.board.dle.search_by_word')
    def test_rae_search(self, mock_search_by_word):
        board = Board()
        valid_word = 'casa'
        mock_search_by_word.return_value.title = 'casa | Definición | Diccionario de la lengua española | RAE - ASALE'
        result1 = board.validate_word(valid_word)
        mock_search_by_word.return_value.title = 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'  
        invalid_word = 'uasffho'
        result2 = board.validate_word(invalid_word)
        self.assertEqual(result1, True)
        self.assertEqual(result2, False)

    def test_put_word(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,7)
        orientation = True
        board.put_word(word,location,orientation)
        self.assertEqual(board.grid[7][7].letter.letter,'c')
        self.assertEqual(board.grid[7][8].letter.letter,'a')
        self.assertEqual(board.grid[7][9].letter.letter,'s')
        self.assertEqual(board.grid[7][10].letter.letter,'a')
    
    def test_put_word_vertical(self):
        board = Board()
        word = [Tile('f',1),Tile('a',1),Tile('c',2),Tile('u',1),Tile('l',1),Tile('t',1),Tile('a',1),Tile('d',1)]
        location = (7,7)
        orientation = False
        board.put_word(word,location,orientation)
        self.assertEqual(board.grid[7][7].letter.letter,'f')
        self.assertEqual(board.grid[8][7].letter.letter,'a')
        self.assertEqual(board.grid[9][7].letter.letter,'c')
        self.assertEqual(board.grid[10][7].letter.letter,'u')
        self.assertEqual(board.grid[11][7].letter.letter,'l')
        self.assertEqual(board.grid[12][7].letter.letter,'t')
        self.assertEqual(board.grid[13][7].letter.letter,'a')
        self.assertEqual(board.grid[14][7].letter.letter,'d')

    def test_put_word_with_intersection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',1)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',2)
        board.grid[7][10].letter = Tile('A',1)
        word = [Tile('S',1)]
        location = (7,7)
        orientation = True
        board.put_word(word,location,orientation)
        self.assertEqual(board.grid[7][7].letter.letter,'C')
        self.assertEqual(board.grid[7][8].letter.letter,'A')
        self.assertEqual(board.grid[7][9].letter.letter,'S')
        self.assertEqual(board.grid[7][10].letter.letter,'A')
        self.assertEqual(board.grid[7][11].letter.letter,'S')

    def test_remove_accent(self):
        board = Board()
        word = 'PAPÁ'
        self.assertEqual(board.remove_accent(word),'PAPA')

    def test_remove_accent_false(self):
        board = Board()
        word = 'PAPA'
        self.assertEqual(board.remove_accent(word),'PAPA')

    def test_get_word_tithout_intersection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',1)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',2)
        board.grid[7][10].letter = Tile('A',1)
        word = 'faca'
        location = (6,8)
        orientation = False
        self.assertEqual(board.get_word_without_intersections(word,location,orientation),'fca')

    def test_one_valid_intesection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',6)
        board.grid[7][10].letter = Tile('A',1)
        word = 'LASO'
        result = board.validate_not_empty(word,(6,10),False)
        self.assertEqual(result, True)

    def test_one_invalid_intesection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',6)
        board.grid[7][10].letter = Tile('A',1)
        word = 'LASO'
        result = board.validate_not_empty(word,(5,10),False)
        self.assertEqual(result, False)

    def test_one_not_intesection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',6)
        board.grid[7][10].letter = Tile('A',1)
        word = 'LASO'
        result = board.validate_not_empty(word,(0,10),False)
        self.assertEqual(result, False)

    def test_word_of_word_valid(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',6)
        board.grid[7][10].letter = Tile('A',1)
        word = 'CASAS'
        location = (7,7)
        orientation = True
        # ipdb.set_trace()
        result = board.validate_not_empty(word,location,orientation)
        self.assertEqual(result, True)

    def test_word_of_word_invalid(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',6)
        board.grid[7][10].letter = Tile('A',1)
        word = 'CASOS'
        result = board.validate_not_empty(word,(7,7),True)
        self.assertEqual(result, False)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_valid_right(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'soso, sosa | Definición | Diccionario de la lengua española | RAE - ASALE'
        board = Board()
        board.grid[7][6].letter = Tile('C',3)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[7][8].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('A',1)
        board.grid[6][9].letter = Tile('L',3)
        board.grid[8][9].letter = Tile('S',6)
        board.grid[9][9].letter = Tile('O',1)
        board.grid[9][8].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('O',1)
        word = 'cosa'
        orientation = False
        location = (7,6)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, True)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_invalid_right(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'  
        board = Board()
        board.grid[7][6].letter = Tile('C',3)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[7][8].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('A',1)
        board.grid[6][9].letter = Tile('L',3)
        board.grid[8][9].letter = Tile('S',6)
        board.grid[9][9].letter = Tile('O',1)
        board.grid[9][8].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('O',1)
        word = 'cono'
        orientation = False
        location = (7,6)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, False)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_valid_left(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'osos | Definición | Diccionario de la lengua española | RAE - ASALE'  
        board = Board()
        board.grid[7][4].letter = Tile('C',3)
        board.grid[7][5].letter = Tile('A',1)
        board.grid[7][6].letter = Tile('S',6)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[7][8].letter = Tile('S',6)
        board.grid[6][5].letter = Tile('L',3)
        board.grid[8][5].letter = Tile('S',6)
        board.grid[9][5].letter = Tile('O',1)
        board.grid[9][6].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('O',1)
        word = 'casos'
        orientation = False
        location = (5,8)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, True)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_invalid_left(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'  
        board = Board()
        board.grid[7][4].letter = Tile('C',3)
        board.grid[7][5].letter = Tile('A',1)
        board.grid[7][6].letter = Tile('S',6)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[7][8].letter = Tile('S',6)
        board.grid[6][5].letter = Tile('L',3)
        board.grid[8][5].letter = Tile('S',6)
        board.grid[9][5].letter = Tile('O',1)
        board.grid[9][6].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('O',1)
        word = 'sopa'
        orientation = False
        location = (7,8)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, False)

    @patch('game.board.dle.search_by_word')
    def test_two_complex_word_validation_invalid_left(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'  
        board = Board()
        board.grid[7][4].letter = Tile('C',3)
        board.grid[7][5].letter = Tile('A',1)
        board.grid[7][6].letter = Tile('S',6)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[6][5].letter = Tile('L',3)
        board.grid[8][5].letter = Tile('S',6)
        board.grid[9][5].letter = Tile('O',1)
        board.grid[9][6].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('O',1)
        word = 'remos'
        orientation = False
        location = (5,8)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, False)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_valid_lower(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'soso, sosa | Definición | Diccionario de la lengua española | RAE - ASALE'
        board = Board()
        board.grid[6][7].letter = Tile('C',3)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[8][7].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('A',1)
        board.grid[9][6].letter = Tile('L',3)
        board.grid[9][8].letter = Tile('S',6)
        board.grid[9][9].letter = Tile('O',1)
        board.grid[8][9].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('O',1)
        word = 'cosa'
        orientation = True
        location = (6,7)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, True)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_invalid_lower(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'  
        board = Board()
        board.grid[6][7].letter = Tile('C',3)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[8][7].letter = Tile('S',6)
        board.grid[9][7].letter = Tile('A',1)
        board.grid[9][6].letter = Tile('L',3)
        board.grid[9][8].letter = Tile('S',6)
        board.grid[9][9].letter = Tile('O',1)
        board.grid[8][9].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('O',1)
        word = 'cono'
        orientation = True
        location = (6,7)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, False)

    @patch('game.board.dle.search_by_word')
    def test_complex_word_validation_valid_up(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'osos | Definición | Diccionario de la lengua española | RAE - ASALE'  
        board = Board()
        board.grid[4][7].letter = Tile('C',3)
        board.grid[5][7].letter = Tile('A',1)
        board.grid[6][7].letter = Tile('S',6)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[8][7].letter = Tile('S',6)
        board.grid[5][6].letter = Tile('L',3)
        board.grid[5][8].letter = Tile('S',6)
        board.grid[5][9].letter = Tile('O',1)
        board.grid[6][9].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('O',1)
        word = 'casos'
        orientation = True
        location = (8,5)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, True)

    @patch('game.board.dle.search_by_word')
    def test_double_complex_word_validation_valid_right_left(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'sus | Definición | Diccionario de la lengua española | RAE - ASALE'  
        board = Board()
        board.grid[4][7].letter = Tile('C',3)
        board.grid[5][7].letter = Tile('A',1)
        board.grid[6][7].letter = Tile('S',6)
        board.grid[7][7].letter = Tile('A',1)
        board.grid[8][7].letter = Tile('S',6)
        board.grid[5][6].letter = Tile('L',3)
        board.grid[5][8].letter = Tile('S',6)
        board.grid[5][9].letter = Tile('O',1)
        board.grid[6][9].letter = Tile('S',6)
        board.grid[7][9].letter = Tile('O',1)
        board.grid[8][5].letter = Tile('C',3)
        board.grid[8][6].letter = Tile('A',1)
        board.grid[8][8].letter = Tile('O',1)
        board.grid[8][9].letter = Tile('S',1)
        word = 'sumo'
        orientation = False
        location = (5,8)
        is_valid = board.validate_not_empty(word, location, orientation)
        self.assertEqual(is_valid, False)

    @patch('game.board.dle.search_by_word')
    def test_validate_all(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'casa | Definición | Diccionario de la lengua española | RAE - ASALE'  
        board = Board()
        word = 'casa'
        orientation = True
        location = (7,7)
        is_valid = board.validate(word,location,orientation)
        self.assertEqual(is_valid, True)

    @patch('game.board.dle.search_by_word')
    def test_validate_all_with_word(self, mock_search_by_word):
        mock_search_by_word.return_value.title = 'casa | Definición | Diccionario de la lengua española | RAE - ASALE'  
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        word = 'casa'
        orientation = True
        location = (7,7)
        is_valid = board.validate(word,location,orientation)
        self.assertEqual(is_valid, True)

    def test_calculate_word_value(self):
        board = Board()
        word = 'faca'
        location = (7,7)
        orientation = False
        self.assertEqual(board.calculate_word_value(word,location,orientation),18)

    def test_calculate_word_value_with_intersection(self):
        board = Board()
        board.grid[7][7].letter = Tile('C',3)
        board.grid[7][8].letter = Tile('A',1)
        board.grid[7][9].letter = Tile('S',2)
        board.grid[7][10].letter = Tile('A',1)
        board.grid[7][7].active = False
        word = 'faca'
        location = (6,8)
        orientation = False
        self.assertEqual(board.calculate_word_value(word,location,orientation),16)
class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(multiplier=2, multiplier_type='letter',)
        self.assertEqual(cell.multiplier,2)
        self.assertEqual(cell.multiplier_type,'letter')
        self.assertIsNone(cell.letter)
        self.assertEqual(cell.calculate_value(),0)


    def test_add_letter(self):
        cell = Cell(multiplier=1, multiplier_type='')
        letter = Tile(letter='p', value=3)
        cell.add_letter(tile=letter)
        self.assertEqual(cell.letter, letter)


    def test_cell_multiplier_letter(self):
        cell = Cell(multiplier=2, multiplier_type='letter')
        letter = Tile(letter='p', value=3)
        cell.add_letter(tile=letter)
        self.assertEqual(cell.calculate_value(),6)

    def test_cell_multiplayer_none(self):
        cell = Cell(multiplier=1, multiplier_type='')
        letter = Tile(letter='p', value=3)
        cell.add_letter(tile=letter)
        self.assertEqual(cell.calculate_value(),3)

    
if __name__ == '__main__':

    unittest.main()