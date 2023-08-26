
import unittest

from GameSC.SC import *

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

        player_1 = Player()

        self.assertEqual(

            len(player_1.tiles),

            0,

        )
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




if __name__ == '__main__':

    unittest.main()

