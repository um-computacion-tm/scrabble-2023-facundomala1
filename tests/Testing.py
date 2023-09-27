
import unittest

from game.SC import Tile, BagTiles, Player, Board, Cell, ScrabbleGame

from unittest.mock import patch

class TestInitialization(unittest.TestCase):
    def test_init(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertIsNotNone(scrabble_game.board)
        self.assertEqual(len(scrabble_game.players), 3)
        self.assertIsNotNone(scrabble_game.bag_tiles)

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
    
    def test_validate_word(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertTrue(scrabble_game.validate_word('hola'))
        self.assertFalse(scrabble_game.validate_word(''))


class TestEnd(unittest.TestCase):
    def test_end_game(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertFalse(scrabble_game.end_game())
        scrabble_game.bag_tiles=[]
        self.assertTrue(scrabble_game.end_game())


class TestTiles(unittest.TestCase):

    def test_tile(self):

        tile = Tile('A', 1)

        self.assertEqual(tile.letter, 'A')

        self.assertEqual(tile.value, 1)


class TestBagTiles(unittest.TestCase):

    @patch('random.shuffle')

    def test_bag_tiles(self, patch_shuffle):

        bag = BagTiles()

        self.assertEqual(

            len(bag.tiles),

            5,

        )

        self.assertEqual(

            patch_shuffle.call_count,

            1,

        )

        self.assertEqual(

            patch_shuffle.call_args[0][0],

            bag.tiles,

        )


    def test_take(self):

        bag = BagTiles()

        tiles = bag.take(2)

        self.assertEqual(

            len(bag.tiles),

            3,

        )

        self.assertEqual(

            len(tiles),

            2,

        )

    def test_put(self):

        bag = BagTiles()

        put_tiles = [Tile('Z', 1), Tile('Y', 1)]

        bag.put(put_tiles)

        self.assertEqual(

            len(bag.tiles),

            7,

        )

class TestPlayer(unittest.TestCase):

    def test_init(self):
        player=Player('Gabriel',0,0,BagTiles())
        self.assertEqual(player.name,'Gabriel')
        self.assertEqual(player.score,0)
        self.assertEqual(player.number,0)
        self.assertEqual(len(player.tiles),0)

    def test_add_tiles(self):
        player=Player('Gabriel',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1)]
        player.add_tiles(tiles)
        self.assertEqual(len(player.tiles),3)
        self.assertEqual(player.tiles[0].letter,'A')
        self.assertEqual(player.tiles[1].letter,'B')
        self.assertEqual(player.tiles[2].letter,'C')

    def test_change_tiles(self):
        player=Player('Gabriel',0,0,BagTiles())
        tiles=[Tile('A',1),Tile('B',1),Tile('C',1)]
        player.add_tiles(tiles)
        print(player.tiles)
        player.change_tiles([1,2],[Tile('D',1),Tile('E',1)])
        self.assertEqual(len(player.tiles),3)
        self.assertEqual(player.tiles[0].letter,'D')
        self.assertEqual(player.tiles[1].letter,'E')
        self.assertEqual(player.tiles[2].letter,'C')

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
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,7)
        orientation = 'H'
        board.put_word(word,location,orientation)
        self.assertEqual(board.is_empty(), False)

    def test_len_of_word_in_board_x(self):
        board = Board()
        word = 'facultad'
        location = (5,4)
        orientation = 'H'
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),True)

    def test_len_of_word_in_board_y(self):
        board = Board()
        word = 'facultad'
        location = (5,4)
        orientation = 'V'
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),True)

    def test_len_of_word_out_of_board_x(self):
        board = Board()
        word = 'facultad'
        location = (10,5)
        orientation = 'H'
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),False)

    def test_len_of_word_out_of_board_y(self):
        board = Board()
        word = 'facultad'
        location = (5,10)
        orientation ='V'
        self.assertEqual(board.validate_len_of_word_in_board(word,location,orientation),False)

    def test_put_word_horizontal_empty(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location =(7,7)
        orientation ='H'
        board.put_word(word,location,orientation)
        self.assertEqual(board.grid[7][7].letter.letter,Tile('c',1).letter)
        self.assertEqual(board.grid[7][8].letter.letter,Tile('a',1).letter)
        self.assertEqual(board.grid[7][9].letter.letter,Tile('s',2).letter)
        self.assertEqual(board.grid[7][10].letter.letter,Tile('a',1).letter)

    def test_put_word_vertical_empty(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,7)
        orientation = 'V'
        board.put_word(word,location,orientation)
        self.assertEqual(board.grid[7][7].letter.letter,Tile('c',1).letter)
        self.assertEqual(board.grid[8][7].letter.letter,Tile('a',1).letter)
        self.assertEqual(board.grid[9][7].letter.letter,Tile('s',2).letter)
        self.assertEqual(board.grid[10][7].letter.letter,Tile('a',1).letter)

    def test_validate_word_in_board_horizontal(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,4)
        orientation = 'H'
        board.put_word(word,location,orientation)
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)

    def test_validate_word_in_board_vertical(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (4,7)
        orientation = 'V'
        board.put_word(word,location,orientation)
        self.assertEqual(board.validate_init_of_game(word,location,orientation),True)

    def test_not_validate_word_in_board_horizontal(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (5,8)
        orientation = 'H'
        board.put_word(word,location,orientation)
        self.assertEqual(board.validate_init_of_game(word,location,orientation),False)

    def test_not_validate_word_in_board_vertical(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (8,5)
        orientation = 'V'
        board.put_word(word,location,orientation)
        self.assertEqual(board.validate_init_of_game(word,location,orientation),False)

    def test_not_empty(self):
        board = Board()
        word0 = [Tile('a',1),Tile('u',1),Tile('t',2),Tile('o',1)]
        location0 = (7,7)
        orientation = 'H'
        board.put_word(word0,location0,orientation)
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (8,7)
        orientation = 'H'
        board.put_word(word,location,orientation)
        self.assertEqual(board.validate_init_of_game(word,location,orientation),False)
        
    def test_show_board(self):
        board = Board()
        board.show_board()

    def test_show_board_with_word(self):
        board = Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,7)
        orientation = 'H'
        board.put_word(word,location,orientation)
        board.show_board()

    def test_show_board_with_words(self):
        board=Board()
        word = [Tile('c',1),Tile('a',1),Tile('s',2),Tile('a',1)]
        location = (7,7)
        orientation = 'H'
        board.put_word(word,location,orientation)
        word1 = [Tile('a',1),Tile('u',1),Tile('t',2),Tile('o',1)]
        location1 = (8,7)
        orientation = 'V'
        board.put_word(word1,location1,orientation)
        board.show_board()




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


    def test_cell_multiplier_word(self):
        cell_1 = Cell(multiplier=1,multiplier_type='letter')
        cell_1.add_letter(Tile('C', 1)) 
        cell_2 = Cell(multiplier=1,multiplier_type='letter')
        cell_2.add_letter(Tile('A', 1))
        cell_3 = Cell(multiplier=3,multiplier_type='word')
        cell_3.add_letter(Tile('S', 2))
        cell_4 = Cell(multiplier=1,multiplier_type='letter')
        cell_4.add_letter(Tile('A', 1))
        word = [cell_1, cell_2, cell_3, cell_4]
        value=Board().calculate_word_value(word)
        self.assertEqual(value,15)


    def test_cell_multiplier_both(self):
        cell_1 = Cell(multiplier=2,multiplier_type='letter')
        cell_1.add_letter(Tile('C', 1)) 
        cell_2 = Cell(multiplier=1,multiplier_type='letter')
        cell_2.add_letter(Tile('A', 1))
        cell_3 = Cell(multiplier=3,multiplier_type='word')
        cell_3.add_letter(Tile('S', 2))
        cell_4 = Cell(multiplier=1,multiplier_type='letter')
        cell_4.add_letter(Tile('A', 1))
        word = [cell_1, cell_2, cell_3, cell_4]
        value=Board().calculate_word_value(word)
        self.assertEqual(value,18)

    def test_cell_multiplier_none(self):
        cell_1 = Cell(multiplier=1,multiplier_type='letter')
        cell_1.add_letter(Tile('C', 1)) 
        cell_2 = Cell(multiplier=1,multiplier_type='letter')
        cell_2.add_letter(Tile('A', 1))
        cell_3 = Cell(multiplier=3,multiplier_type='word')
        cell_3.add_letter(Tile('S', 2))
        cell_4 = Cell(multiplier=1,multiplier_type='letter')
        cell_4.add_letter(Tile('A', 1))
        word = [cell_1, cell_2, cell_3, cell_4]
        value=Board().calculate_word_value(word)
        self.assertEqual(value,15)
        value2=Board().calculate_word_value(word)
        self.assertEqual(value2,5)




if __name__ == '__main__':

    unittest.main()

