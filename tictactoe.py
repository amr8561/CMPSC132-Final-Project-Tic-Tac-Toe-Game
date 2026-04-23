### TIC TAC TOE ###
# Two player tic tac toe game that runs in the terminal. 

rows = [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3']]
columns = [['a1','b1','c1'],['a2','b2','c2'],['a3','b3','c3']]
diagonals = [['a1','b2','c3'],['a3','b2','c1']]

class Board:
    # Board class handles changes to the game board itself. Checks for winners or draws.
    def __init__(self, player1, player2):
        self.board = {'a1': ' ', 'a2': ' ', 'a3': ' ', 'b1': ' ', 'b2': ' ', 'b3': ' ', 'c1': ' ', 'c2': ' ', 'c3': ' '} #Board initializes empty
        self.players = [player1, player2]
        self.turn = 0
        self.draws = 0

    def __str__(self):
        # all board locations are replaced by dictionary values 
        return f'\n    1   2   3\n\nA   {self.board['a1']} | {self.board['a2']} | {self.board['a3']}\n   -----------\nB   {self.board['b1']} | {self.board['b2']} | {self.board['b3']}\n   -----------\nC   {self.board['c1']} | {self.board['c2']} | {self.board['c3']}\n\n'

    __repr__ = __str__

    def clear_board(self):
        self.board = {'a1': ' ', 'a2': ' ', 'a3': ' ', 'b1': ' ', 'b2': ' ', 'b3': ' ', 'c1': ' ', 'c2': ' ', 'c3': ' '}

    def get_pos(self,pos):
        # Function reformats position to match the board dictionary keys. Also checks that a position is valid.
        valid_alpha = ['a','b','c']
        valid_num = ['1','2','3']
        alpha_count = 0
        num_count = 0
        pos = list(pos.lower())
        for char in pos:
            if char in valid_alpha:
                alpha = char
                alpha_count += 1
            elif char in valid_num:
                num = char
                num_count +=1
            elif char == ' ': # Ignore spaces
                pass
            else: # unrecognized character
                raise ValueError
        if alpha_count == 1 and num_count == 1: #If exactly one valid number and one valid letter are provided, the location is valid.
            return ''.join([alpha,num])
        raise ValueError # More than one valid number and letter.
    
    def isEmpty(self,pos):
        # Function checks if a given position on the board is empty. Returns True if so. # Assumes properly formatted pos.
        if self.board[pos] == ' ':
            return True
        return False


    def update_board(self, pos, sym):
        # Places the specified symbol into the specified position on the board. #Assumes properly formatted position.
        self.board[pos] = sym # Update board dictionary
    

    def swap_turn_order(self):
        # Function switches with player is plays the first symbol.
        new_order = [self.players[1],self.players[0]]
        self.players = new_order
        print(f'Turn order swapped! {self.players[0].name} will go first.')



    def check_winner(self):
        # Function checks if there is a winner. Returns False if no. Otherwise, returns self.symbols[0] or self.symbols[1] according to which won.
        # Check rows
        for row in rows:
            if self.board[row[0]] == self.board[row[1]] == self.board[row[2]] and self.board[row[0]] != ' ':
                return self.board[row[0]]
        # Check columns
        for column in columns:
            if self.board[column[0]] == self.board[column[1]] == self.board[column[2]] and self.board[column[0]] != ' ':
                return self.board[column[0]]
        # Check diagonals
        for diagonal in diagonals:
            if self.board[diagonal[0]] == self.board[diagonal[1]] == self.board[diagonal[2]] and self.board[diagonal[0]] != ' ':
                return self.board[diagonal[0]]
        # Otherwise, no winners
        return False

        
    def check_draw(self):
        # Function checks if the board has been completely filled in it. Returns True if it is a draw.
        for cell, symbol in self.board.items():
            if symbol == ' ':
                return False
        return True


    def take_turn(self,pos,player):
        # Function updates board, updates turn counter, and checks for a winner or draw.
        
        self.update_board(pos,player.symbol)
        self.turn += 1
        print(self)

        # Check for a draw
        if self.check_draw():
            self.draws += 1
            print(f"\tIt's a draw!")
            return
        
        #Check for a winner
        winner = self.check_winner()
        # Return if no winner yet
        if not winner:
            return
        # If winner, increment win counter.
        else:
            if winner == self.players[0].symbol: # If the winning symbol was player 1's symbol, player 1 wins
                print(f"{self.players[0].name} wins!\n")
                self.players[0].wins += 1
            else:
                print(f"{self.players[1].name} wins!\n")
                self.players[1].wins += 1
            return




    def play_game(self):
        
        print(self)
        while not self.check_draw() and not self.check_winner(): # loop while there is no winner nor draw
            current_player = self.players[self.turn%2] # Alternates player turn
            valid_input = False
            # Check for valid input on board 
            while not valid_input:
                try:
                    pos = input(f"{current_player.name} ('{current_player.symbol}'), Enter cell: ")
                    pos = self.get_pos(pos)
                    if self.isEmpty(pos):
                        valid_input = True
                    else:
                        print('Cell is full')
                except ValueError:
                    print('Invalid cell')
            # When input is valid, take turn.
            self.take_turn(pos,current_player)

        # If there is a Winner or a Draw:
        self.clear_board() # Clear board to prepare for next game
        self.turn = 0 # Reset turn count
        self.post_game_menu() # move to the post game menu





    def post_game_menu(self):
    # Handles restarting the board, or returning to main  menu after game is finished.
        valid_input = False
        while not valid_input:
            selected = input('Please select an option by entering the corresponding number:\n(1) Play Again\n(2) Play Again with Turn Order Swapped\n(3) Return to Main Menu\n')
            if selected == '1':
                valid_input = True
                self.play_game()
            elif selected == '2':
                valid_input = True
                self.swap_turn_order()
                self.play_game()
            elif selected=='3':
                valid_input = True
                main_menu()
            



class Player:
    # Player class keeps track of wins in a session, symbol associated with player, and turn order (0 plays first, 1 plays second).
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.wins = 0

        
    def __str__(self):
        return f"{self.name}\nSymbol:\t{self.symbol}\nWins:\t{self.wins}"
    
    __repr__ = __str__

    def update_sym(self,other):
        valid = False #get user inputted symbol for self
        while not valid:
            sym1 = input(f'Enter symbol for {self.name}: ')
            if len(sym1) != 1:
                print('Symbol must be one character long')
            elif sym1 == ' ':
                print('Symbol cannot be empty')
            else:
                valid = True              
        valid = False #get user inputted symbol for other,, must be unique
        while not valid:
            sym2 = input(f'Enter symbol for {other.name}: ')
            if len(sym2) != 1:
                print('Symbol must be one character long')
            elif sym2 == ' ':
                print('Symbol cannot be empty')
            elif sym2 == sym1:
                print('The symbols cannot be identical.')
            else:
                valid = True
        self.symbol = sym1
        other.symbol = sym2
        




# Program starts by running main_menu()
def main_menu():
    # Function allows users to select options to edit game preferences or start the game.
    selected = input('\nPlease select an option by entering the corresponding number:\n(1) Play Tic Tac Toe\n(2) Edit Symbols\n(3) Swap Turn Order\n(4) See Current Scores\n(5) Exit Program\n')
    if selected == '1': # Play game
        b.play_game()
    elif selected == '2': # Edit Symbols
        player1.update_sym(player2) #updates both players symbols
        print('Symbols updated!')
        main_menu()
    elif selected == '3': # Swap turn order
        b.swap_turn_order()
        main_menu()
    elif selected == '4': # See Current Scores
        print('\n')
        print(player1, '\n')
        print(player2, '\n')
        print(f"Draws: {b.draws}\n")
        main_menu()
    elif selected == '5': # Exit program
        exit
    else:
        print('\nInvalid Selection\n')
        main_menu()


#Initializes the game:
player1 = Player('Player 1','X')
player2 = Player('Player 2','O')
b = Board(player1,player2)
main_menu() #This line starts the game immediately when the program is run.