import copy   

class Puzzle:
    '''
    Fields:
            size: Nat 
            board: (listof (listof (anyof Str Nat Guess))
            constraints: (listof (list Str Nat (anyof '+' '-' '*' '/' '='))))
    requires: See Assignment Specifications
    '''
    
    def __init__(self, size, board, constraints):
        self.size=size
        self.board=board
        self.constraints=constraints
        
    def __eq__(self, other):
        return (isinstance(other,Puzzle)) and \
            self.size==other.size and \
            self.board == other.board and \
            self.constraints == other.constraints
    
    def __repr__(self):
        s='Puzzle(\nSize='+str(self.size)+'\n'+"Board:\n"
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.board[i][j],Guess):
                    s=s+str(self.board[i][j])+' '
                else:
                    s=s+str(self.board[i][j])+' '*7
            s=s+'\n'
        s=s+"Constraints:\n"
        for i in range(len(self.constraints)):
            s=s+'[ '+ self.constraints[i][0] + '  ' + \
                str(self.constraints[i][1]) + '  ' + self.constraints[i][2]+ \
                ' ]'+'\n'
        s=s+')'
        return s    

class Guess:
    '''
    Fields:
            symbol: Str 
            number: Nat
    requires: See Assignment Specifications
    '''        
    
    def __init__(self, symbol, number):
        self.symbol=symbol
        self.number=number
        
    def __repr__(self):
        return "('{0}',{1})".format(self.symbol, self.number)
    
    def __eq__(self, other):
        return (isinstance(other, Guess)) and \
            self.symbol==other.symbol and \
            self.number == other.number        

class Posn:
    '''
    Fields:
            y: Nat 
            y: Nat
    requires: See Assignment Specifications
    '''         
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)
    
    def __eq__(self,other):
        return (isinstance(other, Posn)) and \
            self.x==other.x and \
            self.y == other.y 


## split(string) consumes a string and splits it, then appends it to a new list 
##               as a number if it is a number, and as a string otherwise
## split: Str -> (listof (anyof Nat, Str))
## Examples:
## split("nicole 7 tam") => ["nicole", 7, "tam"]
## split("a 7 *") => ["a", 7, "*"]

def split(string):
    alist = []
    s = string.split()
    for i in s:
        if i.isdigit():
            alist.append(int(i))
        else:
            alist.append(i)
    return alist
            
    
## read_puzzle(fname) reads information from fname file and returns the info as 
## Puzzle value.
## read_puzzle: Str -> Puzzle
## Example: 
## read_puzzle(

def read_puzzle(fname):
    puzzle = open(fname)
    size = int(puzzle.readline())
    board = []
    for i in range(size):
        newline = puzzle.readline()
        alist = newline.split()
        board.append(alist)
    rest_list = puzzle.readlines()
    constraints = list(map(lambda x: split(x), rest_list))
    puzzle.close()
    return Puzzle(size, board, constraints)
    
    
## print_sol(puz, fname) prints the Puzzle puz in fname file
## print_sol: Puzzle Str -> None

def print_sol(puz, fname):
    sol = open(fname, "w")
    board = puz.board 
    counter = 1
    for i in range(puz.size):
        for l in range(puz.size):
            if puz.size == counter:
                sol.write(str(board[i][l]) + "  \n")
                counter = 1
            else:
                sol.write(str(board[i][l]) + "  ")
                counter += 1
    sol.close()
    return None

    
## find_blank(puz) returns the position of the first blank
## space in puz, or False if no cells are blank.  If the first constraint has
## only guesses on the board, find_blank returns 'guess'.  
## find_blank: Puzzle -> (anyof Posn False 'guess')
## Examples:
## find_blank(puzzle1) => Posn(0 0)
## find_blank(puzzle3partial) => 'guess'
## find_blank(puzzle2soln) => False

def find_blank(puz):
    if puz.constraints == []:
        return False
    else:
        letter = puz.constraints[0][0]
        for row in range(puz.size):
            for i in range(puz.size):
                if puz.board[row][i] == letter:
                    return Posn(i, row)
        return 'guess'
                
    
## used_in_row(puz, pos) returns a list of numbers used in the same 
## row as (x,y) position, pos, in the given puz.  
## used_in_row: Puzzle Posn -> (listof Nat)
## Example: 
## used_in_row(puzzle1,Posn(1,1)) => []
## used_in_row(puzzle1partial2,Posn(0,1)) => [1,2,4]

def used_in_row(puz,pos):
    used = []
    row = pos.y
    for i in range(puz.size):
        if str(puz.board[row][i]).isdigit():
            used = used + [puz.board[row][i]]
        elif isinstance(puz.board[row][i], Guess):
            used = used + [puz.board[row][i].number]
    used.sort()
    return used



## used_in_col(puz, pos) returns a list of numbers used in the same 
## column as (x,y) position, pos, in the given puz.  
## used_in_col: Puzzle Posn -> (listof Nat)
## Examples:
## used_in_col(puzzle1partial2,Posn(1,0)) => [2,3]
## used_in_col(puzzle2soln,Posn(3,5)) => [1,2,3,4,5,6]

def used_in_col(puz,pos):
    used = []
    col = pos.x
    for i in puz.board:
        if isinstance(i[col], int):
            used.append(i[col])
    used.sort()
    return used


##available_vals(puz,pos) returns a list of valid entries for the (x,y)  
## position, pos, of the consumed puzzle, puz.  
## available_vals: Puzzle Posn -> (listof Nat)
## Examples:
## available_vals(puzzle1partial, Posn(2,2)) => [2,4]
## available_vals(puzzle1partial2, Posn(0,1)) => [3]

def available_vals(puz,pos):
    nums_in_col = used_in_col(puz,pos)
    nums_in_row = used_in_row(puz,pos)
    merge = nums_in_col + nums_in_row
    alon = []
    for i in range(1, puz.size+1):
        alon.append(i)
        
    for a in merge:
        if (a in alon):
            alon.remove(a)
    return alon
        


 
## place_guess(brd,pos,val) fills in the (x,y) position, pos, of the board, brd, 
## with the a guess with value, val
## place_guess: (listof (listof (anyof Str Nat Guess))) Posn Nat 
##              -> (listof (listof (anyof Str Nat Guess)))
## Examples:
## See provided tests

def place_guess(brd,pos,val):
    res=copy.deepcopy(brd)  # a copy of brd is assigned to res without any 
                            # aliasing to avoid mutation of brd. 
                            #  You should update res and return it
    letter = res[pos.y][pos.x]
    res[pos.y][pos.x] = Guess(letter, val)
    return res




# fill_in_guess(puz, pos, val) fills in the pos Position of puz's board with 
# a guess with value val
# fill_in_guess: Puzzle Posn Nat -> Puzzle
# Examples: See provided tests

def fill_in_guess(puz, pos, val):
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    tmp=copy.deepcopy(res.board)
    res.board=place_guess(tmp, pos, val)
    return res


## guess_valid(puz) determines if the guesses in puz satisfy their constraint
## guess_valid: Puzzle -> Bool
## Examples: See provided tests

def guess_valid(puz):
    if puz.constraints == []:
        return True 
    alist = []
    valid = puz.constraints[0][1]
    for row in range(puz.size):
        for i in range(puz.size):
            if isinstance(puz.board[row][i], Guess):
                if puz.constraints[0][0] == puz.board[row][i].symbol:
                    alist = alist + [puz.board[row][i].number]     
    if puz.constraints[0][2] == '+':
        return sum(alist) == valid
    if puz.constraints[0][2] == '-':
        return abs(alist[0] - alist[1]) == abs(valid)
    if puz.constraints[0][2] == '*':
        counter = 1
        for i in range(len(alist)):
            counter = counter * alist[i]
        return counter == valid       
    if puz.constraints[0][2] == '/':
        return (alist[0]/alist[1] == valid) or (alist[1]/alist[0]) == valid
    if puz.constraints[0][2] == '=':
        for i in range(len(alist)):
            if alist[i] != valid:
                return False
        return True
        
         

## apply_guess(puz) converts all guesses in puz into their corresponding numbers
## and removes the first contraint from puz's list of contraints
## apply_guess:  Puzzle -> Puzzle
## Examples: See provided tests

def apply_guess(puz):
    # a copy of puz is assigned to res without any 
    # aliasing to avoid mutation of puz. 
    #  You should update res and return it    
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    for row in range(res.size):
        for i in range(res.size):
            if isinstance(res.board[row][i], Guess):
                res.board[row][i] = res.board[row][i].number
    res.constraints = res.constraints[1:]
    return res
            
 



## neighbours(puz) returns a list of next puzzles after puz in
## the implicit graph
## neighbours: Puzzle -> (listof Puzzle)
## Examples: See provided tests

def neighbours(puz):
    # a copy of puz is assigned to tmp without any 
    # aliasing to avoid mutation of puz. 
    tmp=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    if isinstance(find_blank(tmp), Posn):
        possibilities = available_vals(tmp, find_blank(tmp))
        new_puz = []
        for i in possibilities:
            new_puz = new_puz + [fill_in_guess(tmp,find_blank(tmp),i)]
        return new_puz           
    if find_blank(tmp) == False:
        return []
    if find_blank(tmp) == 'guess':
        if guess_valid(tmp):
            return [apply_guess(tmp)]
    return []
    
    
    

## solve_kenken(orig) finds the solution to a KenKen puzzle,
## orig, or returns False if there is no solution.  
## solve-kenken: Puzzle -> (anyof Puzzle False)
## Examples: See provided tests

def solve_kenken(orig):
    to_visit=[]
    visited=[]
    to_visit.append(orig)
    while to_visit!=[] :
        if find_blank(to_visit[0])==False:
            return to_visit[0]
        elif to_visit[0] in visited:
            to_visit.pop(0)
        else:
            nbrs = neighbours(to_visit[0])
            new = list(filter(lambda x: x not in visited, nbrs))
            new_to_visit=new + to_visit[1:] 
            new_visited= [to_visit[0]] + visited
            to_visit=new_to_visit
            visited=new_visited     
    return False

