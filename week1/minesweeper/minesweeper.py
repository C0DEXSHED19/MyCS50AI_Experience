import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count and self.count != 0:
            for cell in self.cells:
                mines.add(cell)
                
        return mines
        
                
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        if self.count == 0:
            for cell in self.cells:
                safes.add(cell)
        
        return safes
    
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
                
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        
       #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        
        row, column = cell
        neighbors = set()
        if row-1 >= 0:
            up = (row-1,column)
            neighbors.add(up)
            if column - 1 >= 0:
                up_left = (row-1,column-1)
                neighbors.add(up_left)
            if column+1 <= 7:
                up_right = (row-1,column+1)           
                neighbors.add(up_right)
        if row+1 <= 7:
            down = (row+1,column)              #checking all neighboring cells
            neighbors.add(down)
            if column - 1 >= 0:
                down_left = (row+1,column-1)
                neighbors.add(down_left)
            if column+1 <= 7:
                down_right = (row+1,column+1)
                neighbors.add(down_right)
        if column-1 >= 0:
            left = (row,column-1)
            neighbors.add(left)
        if column +1 <= 7:
            right = (row,column+1)
            neighbors.add(right)
        
        undetermined_neighbors = set()    
        for c in neighbors:
            if c in self.safes:    #removes determined cells
                continue
            elif c in self.mines:
                count -= 1
            else:
                undetermined_neighbors.add(c)
                
        new_sentence = Sentence(undetermined_neighbors,count)
        self.knowledge.append(new_sentence)
        
        unchanged = False
        while  not unchanged:
            unchanged = True
            
            new_mines = set()
            new_safes = set()
            for sentence in self.knowledge:
                new_mines = new_mines.union(sentence.known_mines())
                new_safes = new_safes.union(sentence.known_safes())
                
            if new_mines:
                unchanged = False
                for mine in new_mines:
                    self.mark_mine(mine)
                    
            if new_safes:
                unchanged = False
                for safe in new_safes:
                    self.mark_safe(safe)
            subset = set()        
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1.cells !=  sentence2.cells:
                        if sentence1.cells.issubset(sentence2.cells):
                            subset = sentence2.cells - sentence1.cells
                            subset_count = sentence2.count - sentence1.count
                            
                            new_s = Sentence(subset,subset_count)
                            if new_s not in self.knowledge:
                                unchanged = False
                                self.knowledge.append(new_s)
                            
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves_available = self.safes - self.moves_made
        if safe_moves_available:
            move = random.choice(list(safe_moves_available))
            return move
        return None
            
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_moves = set()
        for i in range(8):
            for j in range(8):
                cell = (i,j)
                if cell not in self.mines:
                    if cell not in self.moves_made:
                        available_moves.add(cell)
                        
        if available_moves:
            move = random.choice(list(available_moves))
            return move
        
        return None
                    
        raise NotImplementedError
