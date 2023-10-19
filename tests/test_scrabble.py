
import unittest

from game.game_scrabble import ScrabbleGame, TooMuchTiles, Tile, BagTiles, Player, Board, Cell, TOTALTILES, JokerTile, EmptyTiles

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
        self.assertFalse(scrabble_game.validate_word('hola2'))

    def test_show_board(self):
        
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertEqual(scrabble_game.show_board(), scrabble_game.board.show_board())

    def test_show_player_tiles(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.next_turn()
        scrabble_game.distribute_tiles()
        self.assertEqual(scrabble_game.show_player_tiles(), scrabble_game.current_player.show_tiles())


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
        self.assertEqual(
            len(board.grid),
            15,
        )
        self.assertEqual(
            len(board.grid[0]),
            15,
        )
    def test_word_inside_board(self):
         board= Board()
         word = "Facultad"
         location = (5, 4)
         orientation = "H"

         word_is_valid = board.validate_word_inside_board(word, location, orientation)

         assert word_is_valid == True
    

    def test_word_out_of_board(self):
        board = Board()
        word = "Facultad"
        location = (4, 14)
        orientation = "H"
        word_is_valid = board.validate_word_inside_board(word, location, orientation)

        assert word_is_valid == False
    def test_word_inside_board_vertical(self):
      board = Board()
      word = "FACULTAD"
      location = (5, 4)
      orientation = "V"
      word_is_valid = board.validate_word_inside_board(word, location, orientation)     
      assert word_is_valid == True

    def test_board_is_empty(self):
        board = Board()
        board.empty()
        assert board.is_empty == True
         
    def test_board_is_not_empty(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.empty()
        assert board.is_empty == False
        

    def test_place_word_empty_board_horizontal_fine(self):
         board = Board()
         word = "FACULTAD"
         location = (7, 4)
         orientation = "H"
         word_is_valid = board.validate_word_place_board(word, location, orientation)
         assert word_is_valid == True  

    def test_place_word_empty_board_horizontal_wrong(self):
         board = Board()
         word = "FACULTAD"
         location = (2, 4)
         orientation = "H"
         word_is_valid = board.validate_word_place_board(word, location, orientation)
         assert word_is_valid == False
       
    def test_place_word_empty_board_vertical_fine(self):
         board = Board()
         word = "FACULTAD"
         location = (4, 7)
         orientation = "V"
         word_is_valid = board.validate_word_place_board(word, location, orientation)
         assert word_is_valid == True  
    
    def test_place_word_empty_board_vertical_wrong(self):
         board = Board()
         word = "FACULTAD"
         location = (2, 4)
         orientation = "V"
         word_is_valid = board.validate_word_place_board(word, location, orientation)
         assert word_is_valid == False
         
    def test_place_word_not_empty_board_horizontal_fine(self):
         board = Board()
         board.grid[7][7].add_letter(Tile('C', 1))
         board.grid[8][7].add_letter(Tile('A', 1)) 
         board.grid[9][7].add_letter(Tile('S', 1)) 
         board.grid[10][7].add_letter(Tile('A', 1)) 
         word = "FACULTAD"
         location = (8, 6)
         orientation = "H"
         word_is_valid = board.validate_word_place_board(word, location, orientation)
         assert word_is_valid == True  
    
    def test_place_word_not_empty_board_horizontal_not_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[8][7].add_letter(Tile('A', 1)) 
        board.grid[9][7].add_letter(Tile('S', 1)) 
        board.grid[10][7].add_letter(Tile('A', 1)) 
        word = "MISA"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
        
    def test_place_word_not_empty_board_vertical_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[7][8].add_letter(Tile('A', 1)) 
        board.grid[7][9].add_letter(Tile('S', 1)) 
        board.grid[7][10].add_letter(Tile('A', 1)) 
        word = "FACULTAD"
        location = (6, 8)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True
    
    def test_place_word_not_empty_board_vertical_not_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[7][8].add_letter(Tile('A', 1)) 
        board.grid[7][9].add_letter(Tile('S', 1)) 
        board.grid[7][10].add_letter(Tile('A', 1)) 
        word = "MISA"
        location = (6, 8)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
    
    def test_place_word_not_empty_board_horizontal_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[8][7].add_letter(Tile('A', 1)) 
        board.grid[9][7].add_letter(Tile('S', 1)) 
        board.grid[10][7].add_letter(Tile('A', 1)) 
        word = "FACULTAD"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_not_empty_board_horizontal_not_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[8][7].add_letter(Tile('A', 1)) 
        board.grid[9][7].add_letter(Tile('S', 1)) 
        board.grid[10][7].add_letter(Tile('A', 1)) 
        word = "MISA"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
    
    def test_place_word_not_empty_board_vertical_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[7][8].add_letter(Tile('A', 1)) 
        board.grid[7][9].add_letter(Tile('S', 1)) 
        board.grid[7][10].add_letter(Tile('A', 1)) 
        word = "FACULTAD"
        location = (6, 8)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True
    
    def test_place_word_not_empty_board_vertical_not_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[7][8].add_letter(Tile('A', 1)) 
        board.grid[7][9].add_letter(Tile('S', 1)) 
        board.grid[7][10].add_letter(Tile('A', 1)) 
        word = "MISA"
        location = (6, 8)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
    
    def test_place_word_not_empty_board_horizontal_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tile('C', 1))
        board.grid[8][7].add_letter(Tile('A', 1)) 
        board.grid[9][7].add_letter(Tile('S', 1)) 
        board.grid[10][7].add_letter(Tile('A', 1)) 
        word = "FACULTAD"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    



class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(None,True,multiplier=2, multiplier_type='letter')
        self.assertEqual(
            cell.multiplier,
            2,
        )
        self.assertEqual(
            cell.multiplier_type,
            'letter',
        )
        self.assertIsNone(cell.letter)
        self.assertEqual(
            cell.calculate_value(),
            0,
        )

    def test_add_letter(self):
        cell = Cell(None,True,multiplier=1, multiplier_type='')
        letter = Tile(letter='p', value=3)

        cell.add_letter(letter=letter)

        self.assertEqual(cell.letter, letter)

    def test_cell_value(self):
        cell = Cell(None,True,multiplier=2, multiplier_type='letter')
        letter = Tile(letter='p', value=3)
        cell.add_letter(letter=letter)
        self.assertEqual(
            cell.calculate_value(),
            6,
        )

    def test_cell_multiplier_word(self):
        cell = Cell(None,True,multiplier=2, multiplier_type='word')
        letter = Tile(letter='p', value=3)
        cell.add_letter(letter=letter)
        self.assertEqual(
            cell.calculate_value(),
            3,
        )



if __name__ == '__main__':

    unittest.main()

