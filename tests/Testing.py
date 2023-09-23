
import unittest

from game.SC import Tile, BagTiles, Player, Board, Cell



from unittest.mock import patch


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

        self.assertEqual(board.grid[0][0].multiplier,3)
        self.assertEqual(board.grid[0][0].multiplier_type,'word')
        self.assertEqual(board.grid[0][0].letter,None)      

    

class TestCell(unittest.TestCase):

    def test_init(self):
        cell = Cell(multiplier=2, multiplier_type='letter')
        self.assertEqual(cell.multiplier, 2)
        self.assertEqual(cell.multiplier_type, 'letter')
        self.assertIsNone(cell.letter)
        self.assertEqual(cell.calculate_value(), 0)

    def test_add_letter(self):
        cell = Cell(multiplier=1, multiplier_type='')
        letter = Tile(letter='p', value=3)
        cell.add_letter(letter=letter)
        self.assertEqual(cell.letter, letter)

    def test_cell_value(self):
        cell = Cell(multiplier=2, multiplier_type='letter')
        letter = Tile(letter='p', value=3)
        cell.add_letter(letter=letter)
        self.assertEqual(cell.calculate_value(), 6)

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





if __name__ == '__main__':

    unittest.main()

