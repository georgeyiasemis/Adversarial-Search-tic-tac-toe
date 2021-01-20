import numpy as np
import time
class Game:
    
    def __init__(self, m=3, n=3, k=3):
        self.m = m
        self.n = n
        self.k = k
        self.initialize_game()

    def initialize_game(self):
        '''Initializes a new game by setting an empty Board.'''
        
        print('\nNew Game! \n')
        self.current_state = np.array([['*' for i in range(0,self.n)]for j in range (0,self.m)])        
        # Max (X) plays first
        self.player_turn = 'X'

        
    def drawboard(self):
        '''Draws the current state of the Board:
            'X': move of X player
            'O': move of O player
            '*': no move yet
            
            Examples: 
            An empty Board: 
    
               | * | * | * | 
               | * | * | * | 
               | * | * | * | 
            
            A random Board:
                
               | X | O | X | 
               | * | * | * | 
               | * | O | * |  
                
        '''
        print('\nBoard current state:\n ')
        for i in range(0, self.m):
            for j in range(0, self.n):
                if j==0:
                    print('| ', end="")
                print('{} |'.format(self.current_state[i,j]), end=" ")
            print()
        print()
        
    def is_valid(self, x, y):
        '''Checks whether a move is valid:
            Returns False : if x or y are out of bounds or that move is already played
            Returns True : otherwise
        '''
            
        if x < 0 or x > self.m or y < 0 or y > self.n:
            return False
        elif self.current_state[x,y] != '*':
            return False
        else:
            return True
        

    
    def is_terminal(self):
        ''' Checks if the game is terminated:
        Return None if not.
        Return 'X' if 'X' is the winner
        Return 'O' if 'O' is the winner
        Return '*' if it's a draw.'''
        
        xs = np.array(['X'] * self.k)
        os = np.array(['O'] * self.k)
                                
        # Horizontal win
        for i in range(self.m):
            for j in range(self.n - self.k +1):
                row = self.current_state[i,j:j+self.k]
                if all(xs == row):
                    return 'X'
                elif all(os == row):
                    return 'O'
                
        # Vertical win
        for i in range(self.m - self.k + 1):
            for j in range(self.n):
                col = self.current_state[i:i + self.k, j]
                if all(xs == col):
                    return 'X'
                elif all(os == col):
                    return 'O'
                
        # Diagonal win  
        for i in range(self.m - self.k + 1):
            for j in range(self.n - self.k + 1):
                sub_board = self.current_state[i:i + self.k, j:j + self.k]
                diag1 = []
                diag2 = []
                for z in range(self.k):
                    diag1.append(sub_board[z,z])
                    diag2.append(sub_board[z,self.k - z - 1])
                if all(xs == diag1) or all(xs == diag2):
                    return 'X'
                elif all(os == diag1) or all(os == diag2):
                    return 'O'
                
        # Is Board full?        
        for i in range(self.m):
            for j in range(self.n):
            # There's an empty field, we continue the game
                if (self.current_state[i,j] == '*'):
                    return None
                
        # If none of the above is true, then it's a draw!       
        return '*'
        

    def max(self):
        '''Find the optimal move for max (X).
        Return: (reward, x-coord, y-coord).'''    
        # Utility function for max:
        # -1 loss
        # 0  draw
        # 1  win
    
        # Set v as -Inf initially
        v = -float('Inf')
        # Check if game has ended and return utility;    
        outcome = self.is_terminal()
        if outcome == 'X':
            return (1, None, None)
        elif outcome == 'O':
            return (-1, None, None)
        elif outcome == '*':
            return (0, None, None)
    
        for i in range(0, self.m):
            for j in range(0, self.n):
                if self.current_state[i,j] == '*':
                    self.current_state[i,j] = 'X'
                    (V, _, _) = self.min()
                    # Fix v to maximum
                    if V > v:
                        v = V
                        x = i
                        y = j
                    # Setting back the field to empty
                    self.current_state[i,j] = '*'
        return (v, x, y)
    
    
    def min(self):
        '''Find the optimal move for min (O).
        Return: (reward, x-coord, y-coord)'''
    
        # Utility function for min:
        # -1 X wins
        # 0  draw
        # 1  X looses
        
        # Set v as Inf initially
        v = float('Inf')
        
        # Check if game has ended and return utility;  
        outcome = self.is_terminal()
    
        if outcome == 'X':
            return (1, None, None)
        elif outcome == 'O':
            return (-1, None, None)
        elif outcome == '*':
            return (0, None, None)
    
        for i in range(0, self.m):
            for j in range(0, self.n):
                if self.current_state[i,j] == '*':
                    self.current_state[i,j] = 'O'
                    (V, _, _) = self.max()
                    # Fix v to minimum
                    if V < v:
                        v = V
                        x = i
                        y = j
                    self.current_state[i,j] = '*'
    
        return (v, x, y)
    
    def play(self):
        '''
        Impliments the Minimax algorithm:
        Suggests the optimal action for X (max) and chooses the optimal action 
        for O (min).
        '''
        while True:
            self.drawboard()
            self.outcome = self.is_terminal()
    
            # Printing the appropriate message if the game has ended
            if self.outcome != None:
                if self.outcome == 'X':
                    print('The winner is X!')
                elif self.outcome == 'O':
                    print('The winner is O!')
                elif self.outcome == '*':
                    print("Draw!")
                return
            
            # If max's turn
            if self.player_turn == 'X':
                while True:
                    start = time.time()
                    (_, x, y) = self.max()
                    end = time.time()
                    print('Evaluation time: {} seconds'.format(round(end - start, 5)))
                    print('Recommended action: x = {}, y = {}'.format(x, y))
                    # Ask user to input action for Max
                    x = int(input('Insert the x-coordinate: '))
                    y = int(input('Insert the y-coordinate: '))
                    (x, y) = (x, y)
                    
                    # Check if given action is valid, then take action for max (X); otherwise repeat
                    if self.is_valid(x, y):
                        self.current_state[x,y] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Not a valid move! Try again.')
            # If min's turn
            else:
                start = time.time()
                (_, x, y) = self.min()
                end = time.time()
                print('Evaluation time: {} seconds'.format(round(end - start, 5)))
                # Take action for min (O)
                self.current_state[x,y] = 'O'
                self.player_turn = 'X'
        
    def max_ab(self, a, b):
        '''Find the optimal move for max (X) using # Alpha-Beta Pruning.
        Return: (reward, x-coord, y-coord)'''
        # Utility function for max:
        # -1 loss
        # 0  draw
        # 1  win
        v = -float('Inf')
        # Check if game has ended and return utility;    
        outcome = self.is_terminal()
        if outcome == 'X':
            return (1, None, None)
        elif outcome == 'O':
            return (-1, None, None)
        elif outcome == '*':
            return (0, None, None)
        
        for i in range(0, self.m):
            for j in range(0, self.n):
                if self.current_state[i,j] == '*':
                    self.current_state[i,j] = 'X'
                    (V, _, _) = self.min_ab(a, b)
                    # Fix v to maximum
                    if V > v:
                        v = V
                        x = i
                        y = j
                    # Setting back the field to empty
                    self.current_state[i,j] = '*'
                    
                    if v >= b:
                        return (v, x, y)
                    if v > a:
                        a = v
        return (v, x, y)
    
    def min_ab(self, a, b):
            '''Find the optimal move for min (O) using # Alpha-Beta Pruning
            Return: (reward, x-coord, y-coord)'''
            # Utility function for min:
            # -1 X wins
            # 0  draw
            # 1  X looses
            
            # Set v as Inf initially
            v = float('Inf')
            
            # Check if game has ended and return utility;  
            outcome = self.is_terminal()
        
            if outcome == 'X':
                return (1, None, None)
            elif outcome == 'O':
                return (-1, None, None)
            elif outcome == '*':
                return (0, None, None)
        
            for i in range(0, self.m):
                for j in range(0, self.n):
                    if self.current_state[i,j] == '*':
                        self.current_state[i,j] = 'O'
                        (V, _, _) = self.max()
                        # Fix v to minimum
                        if V < v:
                            v = V
                            x = i
                            y = j
                        self.current_state[i,j] = '*'
                        
                        if v <= a:
                            return (v, x, y)
                        
                        if v < b:
                            b = v
        
            return (v, x, y)
        
    def play_ab(self):
        '''
        Impliments the Alpha-Beta prunning algorithm:
        Suggests the optimal action for X (max) and chooses the optimal action 
        for O (min) using AB-prunning.
        '''
        # Alpha-Beta Prunning
        a = - float('Inf')
        b = float('Inf')
        while True:
            self.drawboard()
            self.outcome = self.is_terminal()
    
            # Printing the appropriate message if the game has ended
            if self.outcome != None:
                if self.outcome == 'X':
                    print('The winner is X!')
                elif self.outcome == 'O':
                    print('The winner is O!')
                elif self.outcome == '*':
                    print("Draw!")
                return
            
            # If max's turn
            if self.player_turn == 'X':
                while True:
                    start = time.time()
                    (_, x, y) = self.max_ab(a, b)
                    end = time.time()
                    print('Evaluation time: {} seconds'.format(round(end - start, 5)))
                    print('Recommended action: x = {}, y = {}'.format(x, y))
                    x = int(input('Insert the x-coordinate: '))
                    y = int(input('Insert the y-coordinate: '))
                    (x, y) = (x, y)
    
                    if self.is_valid(x, y):
                        self.current_state[x,y] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Not a valid move! Try again.')
            # If min's turn
            else:
                start = time.time()
                (_, x, y) = self.min_ab(a, b)
                end = time.time()
                print('Evaluation time: {} seconds'.format(round(end - start, 5)))
                self.current_state[x,y] = 'O'
                self.player_turn = 'X'
            
def main():
    
    tictac = Game(3,3,3)
    # MiniMax
    #tictac.play()
    # Ab pruning
    tictac.play_ab()
    
if __name__ == "__main__":
    main()
