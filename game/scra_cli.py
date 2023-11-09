from game.game_scrabble import *
import os

class GameInterface:

    def __init__(self):
        print('Bienvenidos a Scrabble')
        self.player_count = self.add_players()
        self.scrabble = ScrabbleGame(self.player_count)
        i = 1
        for player in self.scrabble.players:
            player.name = input(f'Nombre del jugador {i}: ')
            player.add_tiles(self.scrabble.tilebag.draw_tiles(7))
            i += 1
        self.scrabble.next_turn()

    def add_players(self):
        try:
            number_of_players = int(input('Ingrese el número de jugadores: '))
            return number_of_players if (number_of_players > 1 and number_of_players) < 4 else ValueError
        except:
            print('Ingrese un número de jugadores válido')
            return self.add_players()

    def play(self):
        board = self.scrabble.board
        while not self.end_game():
            for i in range(len(self.scrabble.players)):
                current_player = self.scrabble.current_player
                print(f'Es el turno de {current_player.name}')
                print(f'La Ronda es: {self.scrabble.round}')
                print(f'Las fichas restantes son: {len(self.scrabble.tilebag.tiles)}')
                print(f'Los puntos de {current_player.name} son: {current_player.score}')
                print('El tablero es:')
                print(board.show_board())
                print(f'El jugador {current_player.name} tiene las siguientes fichas:')
                print(current_player.show_tiles())
                print('Ingrese el numero de la opción que desea realizar')
                print('1. Jugar')
                print('2. Cambiar fichas')
                print('3. Pasar turno')
                print('4. Si posee comodín, ingrese la letra que desea que represente')
                print('5. Terminar juego')
                option = str(input())
                flag = True
                self.handle_option(option,flag)
                
    def handle_option(self, option,flag):
            if option == '1':
                flag = self.play_turn()
            elif option == '2':
                flag = self.change_tiles()
            elif option == '3':
                self.scrabble.current_player.surrender += 1
                pass
            elif option == '4':
                self.select_letter()
            elif option == '5':
                self.scrabble.tilebag.tiles = []
                for player in self.scrabble.players:
                    player.tiles = []
            else:
                print('Ingrese una opción válida')
                flag = False

            print('Presione enter para continuar')
            input()
            if flag:
                self.scrabble.next_turn()
            os.system('clear')
                
    def play_turn(self):
        invalid = True
        while invalid:
            invalid = False
            print('Ingrese la palabra que desea jugar con sus fichas o 5 para salir:')
            print(self.scrabble.current_player.show_tiles())
            word = str(input()).lower()
            if word == '5':
                return False
            print('Ingrese la coordenada de la fila')
            try:
                row = int(input())
            except:
                print('Ingrese una coordenada válida')
                invalid = True
            print('Ingrese la coordenada de la columna')
            try:
                column = int(input())
            except:
                print('Ingrese una coordenada válida')
                invalid = True
            if not invalid:
                location = (row,column)
                print('Ingrese la orientación en la que desea jugar la palabra')
                print('1. Horizontal')
                print('2. Vertical')
                orientation = input()
                orientation = orientation == '1'
                invalid = self.put_word(word,location,orientation)

    def put_word(self, word, location, orientation):
        if self.scrabble.board.validate(word,location,orientation):
            word_no_intersections = self.scrabble.board.get_word_without_intersections(word,location,orientation)
            player = self.scrabble.current_player
            if player.has_tiles(word_no_intersections):
                tiles = player.take_tiles(word_no_intersections)
                player.add_tiles(self.scrabble.tilebag.draw_tiles(len(word_no_intersections)))
                self.scrabble.board.put_word(tiles,location,orientation)
                print(self.scrabble.board.show_board())
                player.score += self.scrabble.board.calculate_word_value(word,location,orientation)
                print(f'Su puntaje es: {player.score}')
                self.scrabble.next_turn()
                return False
            if self.scrabble.board.validate_len_of_word_in_board(word,location,orientation):
                print('Las palabra no entra en el tablero')
                return True
            elif self.scrabble.board.validate_word(word):
                print('La palabra no es válida')
            else:
                print('No tiene las fichas para jugar la palabra')
        return True

    def change_tiles(self):
        print(f'{self.scrabble.current_player.name} Estas son sus fichas:')
        print(self.scrabble.current_player.show_tiles())
        print('Ingrese las posicion de las fichas que desea cambiar o 8 para salir')
        positions = input()
        if positions == '8':
            self.play()
            return False
        positions = positions.split(',')
        positions = [int(position) for position in positions]
        new_tiles = self.scrabble.tilebag.draw_tiles(len(positions))
        self.scrabble.tilebag.put_tiles(new_tiles)
        old_tiles = self.scrabble.change_tiles(positions)
        self.scrabble.tilebag.put_tiles(old_tiles)
        self.scrabble.tilebag.shuffle()
        print('Se han cambiado las fichas')
        print(self.scrabble.current_player.show_tiles())
        return True

    def select_letter(self):
        print('Ingrese la letra que desea que represente el comodín o enter para salir')
        letter = input()
        if letter == '\n':
            return self.play()
        for tile in self.scrabble.current_player.tiles:
            if tile.letter == '_':
                tile.letter = letter.upper()
                print('Se ha cambiado la letra del comodín')
                print(self.scrabble.current_player.show_tiles())
                return
            
    def end_game(self):
        if self.scrabble.end_game():
            print('Gracias por jugar')
            print('Los puntajes son:')
            for player in self.scrabble.players:
                print(f'{player.name}: {player.score}')
            return True


if __name__ == '__main__':
    game = GameInterface()
    game.play()