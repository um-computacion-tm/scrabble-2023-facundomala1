from unittest.mock import patch
from game.scra_cli import *
from game.game_scrabble import *
import unittest
import io, sys

class TestGameInterface(unittest.TestCase):

    @patch('game.scar_cli.GameInterface.add_players', return_value=2)
    @patch('builtins.input', side_effect=['Player 1', 'Player 2'])
    @patch('game.scra_cli.GameInterface.play', return_value='')
    def test_init(self, mock_add_players, mocked_input, mock_play):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        sys.stdout = sys.__stdout__
        output_buffer.close()
        self.assertEqual(len(game_interface.scrabble.players), 2)
        self.assertEqual(game_interface.scrabble.players[0].name, 'Player 1')
        self.assertEqual(game_interface.scrabble.players[1].name, 'Player 2')
        self.assertEqual(len(game_interface.scrabble.players[0].tiles), 7)
        self.assertEqual(len(game_interface.scrabble.players[1].tiles), 7)
        self.assertEqual(len(game_interface.scrabble.tilebag.tiles), 100-14)
        self.assertEqual(game_interface.scrabble.current_player, game_interface.scrabble.players[0])

    @patch('builtins.input', side_effect=['2','1', '2'])
    @patch('game.scra_cli.GameInterface.play', return_value='')
    def test_add_players(self, mocked_input, mock_play):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = ()
        sys.stdout = sys.__stdout__
        output_buffer.close()
        self.assertEqual(len(game_interface.scrabble.players), 2)

    @patch('builtins.input', side_effect=['a',2,'a','b'])
    def test_add_players_invalid(self,mock_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second',5,'\n',5,'\n'])
    def test_play(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.scrabble.current_player.tiles = [Tile('A',1),Tile('A',1),Tile('A',1),Tile('A',1),Tile('A',1),Tile('A',1),Tile('A',1)]
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface.play()
        sys.stdout = sys.__stdout__
        printed_output = output_buffer.getvalue()
        output_buffer.close()
        expected = '''Es el turno de first
La Ronda es: 1
Las fichas restantes son: 86
Los puntos de first son: 0
El tablero es:
       
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

El jugador first tiene las siguientes fichas:
['A', 'A', 'A', 'A', 'A', 'A', 'A']
Ingrese el numero de la opción que desea realizar
1. Jugar
2. Cambiar fichas
3. Pasar turno
4. Si posee comodín, ingrese la letra que desea que represente
5. Terminar juego
Presione enter para continuar
Es el turno de second
La Ronda es: 1
Las fichas restantes son: 0
Los puntos de second son: 0
El tablero es:
       
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

El jugador second tiene las siguientes fichas:
[]
Ingrese el numero de la opción que desea realizar
1. Jugar
2. Cambiar fichas
3. Pasar turno
4. Si posee comodín, ingrese la letra que desea que represente
5. Terminar juego
Presione enter para continuar
Gracias por jugar
Los puntajes son:
first: 0
second: 0
'''
        self.maxDiff = None
        self.assertEqual(printed_output, expected)

    @patch('builtins.input', side_effect=[2,'first','second','\n'])
    def test_handle_option_1(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        with patch.object(game_interface, 'play_turn') as mock_play_turn:
            game_interface.handle_option('1',True)
            mock_play_turn.assert_called_once()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second','\n'])
    def test_handle_option_2(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        with patch.object(game_interface, 'change_tiles') as mock_change_tiles:
            game_interface.handle_option('2',True)
            mock_change_tiles.assert_called_once()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second','\n'])
    def test_handle_option_3(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.handle_option('3',True)
        sys.stdout = sys.__stdout__
        output_buffer.close()
        self.assertEqual(game_interface.scrabble.players[0].surrender, 1)

    @patch('builtins.input', side_effect=[2,'first','second','\n'])
    def test_handle_option_4(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        with patch.object(game_interface, 'select_letter') as mock_select_letter:
            game_interface.handle_option('4',True)
            mock_select_letter.assert_called_once()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second','\n'])
    def test_handle_option_invalid(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.handle_option('6',True)
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second','sopa',7,7,'1','\n'])
    def test_play_turn(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.scrabble.current_player.tiles=[Tile('S',1),Tile('O',1),Tile('P',1),Tile('A',1),Tile('S',1),Tile('S',1),Tile('S',1)]
        game_interface.play_turn()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    @patch('builtins.input', side_effect=[2,'first','second','5','\n'])
    def test_play_turn_cancel(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.scrabble.current_player.tiles=[Tile('S',1),Tile('O',1),Tile('P',1),Tile('A',1),Tile('S',1),Tile('S',1),Tile('S',1)]
        result = game_interface.play_turn()
        sys.stdout = sys.__stdout__
        output_buffer.close()
        self.assertEqual(result, False)

    @patch('builtins.input', side_effect=[2,'first','second','sopa','a',7,'sopa',7,'a','sopa',7,7,'1','\n'])
    def test_play_turn_try_invalid_options(self, mock_init_input):
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        game_interface = GameInterface()
        game_interface.scrabble.current_player.tiles=[Tile('S',1),Tile('O',1),Tile('P',1),Tile('A',1),Tile('S',1),Tile('S',1),Tile('S',1)]
        game_interface.play_turn()
        sys.stdout = sys.__stdout__
        output_buffer.close()

    # @patch('builtins.input', side_effect=[2,'first','second','sopa',7,7,'1','\n'])
    # @patch()
    # def test_put_word(self, mock_init_input):
    #     output_buffer = io.StringIO()
    #     sys.stdout = output_buffer
    #     game_interface = GameInterface()
    #     game_interface.scrabble.current_player.tiles=[Tile('S',1),Tile('O',1),Tile('P',1),Tile('A',1),Tile('S',1),Tile('S',1),Tile('S',1)]
    #     game_interface.put_word('casa',(7,7),True)
    #     sys.stdout = sys.__stdout__
    #     output_buffer.close()