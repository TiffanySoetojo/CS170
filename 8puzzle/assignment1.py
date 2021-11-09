#from nPuzzle import uniform_cost_search
#import matplotlib.pyplot as plt
import copy
import time
import sys


def main():
    print('\n||||||||||||||||||||MAIN MENU||||||||||||||||||||||||||||' +
        '\n\tHello, this is Tiffany\'s 8-puzzle solver.\n'+
        '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n' )

    #set the variables
    viable_input = False

    #let them choose to make a 8-puzzle themselves
    inputPuzzle = input('Type \'1\' if you\'d like a default 8-puzzle, else press \'2\'.'
                    + '\n')
    while viable_input ==False:
        if inputPuzzle == '1':
            print('||||||||Puzzle levels|||||||\n1: Depth 0')
            depth0_puzzle = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']) # this based on the example that prof gave
            print_puzzle(depth0_puzzle)

            #these are the list of different depths
            print('\n2: Depth 2')
            depth2_puzzle = (['1', '2', '3'], ['4', '5', '6'], ['0', '7', '8']) #based on the example that prof gave
            print_puzzle(depth2_puzzle)

            print('\n3: Depth 4')
            depth4_puzzle = (['1', '2', '3'], ['5', '0', '6'], ['4', '7', '8']) #based on the example that prof gave
            print_puzzle(depth4_puzzle)

            print('\n4: Depth 8')
            depth8_puzzle = (['1', '3', '6'], ['5', '0', '2'], ['4', '7', '8']) #based on the example that prof gave
            print_puzzle(depth8_puzzle)

            print('\n5: Depth 12')
            depth12_puzzle = (['1', '3', '6'], ['5', '0', '7'], ['4', '8', '2']) #based on the example that prof gave
            print_puzzle(depth12_puzzle)

            print('\n6: Depth 16')
            depth16_puzzle = (['1', '6', '7'], ['5', '0', '3'], ['4', '8', '2']) #based on the example that prof gave
            print_puzzle(depth16_puzzle)

            print('\n7: Depth 20')
            depth20_puzzle = (['7', '1', '2'], ['4', '8', '5'], ['6', '3', '0']) #based on the example that prof gave
            print_puzzle(depth20_puzzle)

            print('\n8: Depth 24')
            depth24_puzzle = (['0', '7', '2'], ['4', '6', '1'], ['3', '5', '8']) #based on the example that prof gave
            print_puzzle(depth24_puzzle)


            puzzle_level = input('Which level do you want to select? 1 for Depth0, 2 for Depth2, 3 for Depth4, 4 for Depth8, 5 for Depth12, 6 for Depth16, 7 for Depth 20, 8 for Depth 24. \n')

            if(puzzle_level == '1'):
                puz = depth0_puzzle
            elif(puzzle_level == '2'):
                puz = depth2_puzzle
            elif(puzzle_level == '3'):
                puz = depth4_puzzle
            elif(puzzle_level == '4'):
                puz = depth8_puzzle
            elif(puzzle_level == '5'):
                puz = depth12_puzzle
            elif(puzzle_level == '6'):
                puz = depth16_puzzle
            elif(puzzle_level == '7'):
                puz = depth20_puzzle
            elif(puzzle_level == '8'):
                puz = depth24_puzzle
            
            viable_input = True
        #this should implement puzzles that aren't 3by3... in progress, need to update the check_puzzle function and the row 1, 2, 3,... to implement more than 3 rows.
        # for grading, disregard but for future reference, for loop maybe? and then submit the row into the puz and have puz += row... YES
        elif inputPuzzle == '2':
            print('\nIs this an 8-puzzle?')
            eightpuz = input('Type \'y\' for yes and \'n\' for no.\n')
            
            if eightpuz == 'y':

                print('Enter your puzzle, use a zero to represent the blank \n')

                # Getting the first row
                row1 = input('Enter the first row, use spaces between numbers: ')

                # Getting the second row
                row2 = input('Enter the second row, use spaces between numbers: ')

                # Getting the third row
                row3 = input('Enter the third row, use spaces between numbers: ')

                print('\n')

                # Combining input into a puzzle
                row1 = row1.split(' ')
                row2 = row2.split(' ')
                row3 = row3.split(' ')

                puz = row1, row2, row3
                print_puzzle(puz) #prints the puzzle so the user can see
                check_puzzle(puz) #checks if the puzzle has numbers only from 0-8
                viable_input = True
            
            else:
                print('Sorry, there will be future implementation for different puzzles. Return to main menu.')
                main()


        else:
            print('Please output a viable input, i.e. \'1\', \'2\'.\n')
            viable_input = False



    # Allowing the user to choose algorithm
    choice_algorithm = input('Enter your choice of algorithm' 
                 '\n1. Uniform Cost Search '
                 '\n2. A* with the Misplaced Tile heuristic.' 
                 '\n3. A* with the Manhattan distance heuristic\n')
    choice = int(choice_algorithm)
    print(choice)
    if int(choice) == 1 or int(choice) == 2 or int(choice) == 3:
        # Running the program and printing the output

        print(generalsearch(puz, choice))

    else:
        print('Please output a viable input, i.e. \'1\', \'2\', \'3\'.\n')
        main()


#def select_Algorithm():

#main "driver" search algorithm
def generalsearch(puz, choice):

    # This is the pseudo-code that was provided FOLLOW THIS
        #nodes = MAKE_QUEUE(MAKE_NODE(problem.initial-state)) 
        # loop do
        # if EMPTY(Nodes) then return "failure"
        #   node = REMOVE_FRONT(nodes)
        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        #   nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))  
        # end   
    
    #stops alg's if time is over 20 minutes
    # https://www.programiz.com/python-programming/time
    timing = time.time()
    duration = 1200

    goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0] ]

    #https://www.codecademy.com/learn/learn-data-structures-and-algorithms-with-python/modules/nodes/cheatsheet
    #gotta define first
    queue_arr= []
    visited = []
    #g will be 0 once it checks expanded
    g = -1 
    queue_size = 0
    #max starts -1 because will surpass queue
    max_queue = -1

    if choice == 1 :
        #cause uniform 
        h = 0
    elif choice == 2 :
        h = misplaced(puz, goal_puzzle)
    elif choice == 3:
        h = manhattan(puz, goal_puzzle)

    #the parent node
    parent = node(puz)
    parent.cost = h
    parent.depth = 0
    queue_arr.append(parent)
    #the length of the queue is now one
    visited.append(parent.puzzle)
    queue_size +=1
    max_queue +=1
    
    #will loop until a return or exit.
    while True:
        if choice != 1:
            #https://docs.python.org/3/howto/sorting.html
            #an example:
            #>>> student_tuples = [
            # ...     ('john', 'A', 15),
            # ...     ('jane', 'B', 12),
            # ...     ('dave', 'B', 10),
            # ... ]
            # >>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
            # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
            queue_arr = sorted(queue_arr, key = lambda l: (l.depth + l.cost, l.depth))

        if(len(queue_arr) == 0):
            return 'Failure' #exits

        #   node = REMOVE_FRONT(nodes)
        first_node = queue_arr.pop(0)
        if first_node.expanded is False:
            g += 1
            first_node.expanded = True
        queue_size -= 1



        top = expand(first_node, visited)
        direction = [top.nleft, top.nright, top.nup, top.ndown]

        #place all the states of the node into the queue_arr and place the node into the visited
        for i in direction:
            if not i is None:
                if choice == 1:
                    i.cost = 0
                    i.depth = first_node.depth + 1
                elif choice == 2:
                    i.cost = misplaced(i.puzzle, goal_puzzle)
                    i.depth = first_node.depth + 1
                elif choice == 3:
                    i.cost = manhattan(i.puzzle,goal_puzzle)
                    i.depth = first_node.depth + 1
                
                # Add these states to the queue and add them to a list of states we have now visited
                visited.append(i.puzzle)
                queue_arr.append(i)
                queue_size += 1

        # max queue size = queue if max is smaller than queue
        if queue_size > max_queue:
            max_queue = queue_size
        
        # If we make it to goal state print some data
        if g == 0:
            #gotta print out traceback
            print('\nThe best state to expand with a g(n) = ' + str(first_node.depth) + ' and h(n) = ' + str(first_node.cost) + ' is...\n', end = "" )
            # print_puzzle(first_node.puzzle)
            print('Expanding state:\n')
            print_puzzle(first_node.puzzle)
            print('\n')

        elif g != 0:
            print('\nThe best state to expand with a g(n) = ' + str(first_node.depth) + ' and h(n) = ' + str(first_node.cost) + ' is...\n', end = "" )
            print_puzzle(first_node.puzzle)
            print('Expanding this node...\n')

            if is_it_goal(first_node.puzzle, goal_puzzle):
                return ('Goal State! \n\nExpanded nodes:' + str(g) + '\nMax number of nodes in queue:' + str(max_queue) + '\nDepth:' + str(first_node.depth))
                exit

        #so my computer doesn't die
        if time.time() > timing + duration:
            print('Over 20 minutes')
            sys.exit()


def expand(first_node, visited):
    #navigate the empty tile, it is much simpler operate than "move 1 to left" according to slide
    # returns a list of paths we can take that are LEGAL
    # how do I check if we've already visited the state?

    #initialize row and column
    row = 0
    column = 0

    #go through the given puzzle and find empty tile
    for i in range(len(first_node.puzzle)):
        for j in range(len(first_node.puzzle)):
            #current_tile = int(first_node.puzzle[i][j])
            if int(first_node.puzzle[i][j]) == 0:   
                row = i
                column = j
    
    # if we are not on the first column, we can move the empty tile to the left 
    #  1  _  2  ->  _  1  2
    if column >0:
        # call the left function
        first_node = left(first_node, row, column,visited)

    # if we are not at the last column, move right
    if column < len(first_node.puzzle)-1:
        first_node = right(first_node, row, column,visited)

    # if not at the last row, move down
    if row < len(first_node.puzzle)-1:
        first_node = down(first_node, row, column,visited)

    #if not at the first row, move up
    if row > 0:
        first_node = up(first_node, row, column,visited)
    
    return first_node


def left(first_node, row, column, visited):
    # gotta copy the puzzle
    current_format = copy.deepcopy(first_node.puzzle)
    tempRC = current_format[row][column]
    # and then we want the actual empty tile to move
    # to the left is column -1
    current_format[row][column] = current_format[row][column-1]
    # time to flip the two tiles   _  1 -> 1  _
    current_format[row][column-1] = tempRC

    if current_format not in visited:
        first_node.nleft = node(current_format)

    return first_node

def right(first_node, row, column,visited):
    #gotta copy the puzzle
    current_format = copy.deepcopy(first_node.puzzle)
    tempRC = current_format[row][column]
    # and then we want the actual empty tile to move
    # to the right is column + 1
    current_format[row][column] = current_format[row][column+1]
    # time to flip the two tiles   1  _ -> _  1 
    current_format[row][column+1] = tempRC

    if current_format not in visited:
        first_node.nright = node(current_format)
    return first_node


def down(first_node, row, column, visited):
    #gotta copy the puzzle
    current_format = copy.deepcopy(first_node.puzzle)
    tempRC = current_format[row][column]
    # and then we want the actual empty tile to move
    # to the up is row -1
    current_format[row][column] = current_format[row + 1][column]
    # time to flip the two tiles  
    current_format[row +1][column] = tempRC

    if current_format not in visited:
        first_node.ndown = node(current_format)

    return first_node


def up(first_node, row, column,visited):
    #gotta copy the puzzle
    current_format = copy.deepcopy(first_node.puzzle)
    tempRC = current_format[row][column]
    # and then we want the actual empty tile to move
    # to the up is row + 1
    current_format[row][column] = current_format[row - 1][column]
    # time to flip the two tiles  
    current_format[row - 1][column] = tempRC

    if current_format not in visited:
        first_node.nup = node(current_format)
    
    return first_node


#go through the puzzle and take the sum of the moves it takes to go to the goal
#https://www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/
def manhattan(puz, goal):
    print('Current puzzle:')
    print_puzzle(puz)

    #omg you gotta initialize smh
    #counter is basically h(n)
    counter, row, column, goal_row, goal_column = 0,0,0,0,0 

    for x in range(1,9): #this is 1,2,3,4,5,6,7,8
        for i in range(len(puz)):
            for j in range(len(puz)):
                #inside the embedded for loop sum += (abs(x[i] - x[j]) + abs(y[i] - y[j])), gotten from the above link
                # sum+=(abs(row - goalrow) + abs(column + goalcolumn) )
                # need a variable to store i and j for instances in which the puzzle(s) is correct 
                if int(puz[i][j]) == x:
                    row = i
                    column = j
                if goal[i][j] == x:
                    goal_row = i
                    goal_column = j
        counter += abs(row - goal_row) + abs(column - goal_column)

    print('The h(n) is ' + str(counter) + '\n')
    return counter
 

#go through the puzzle and add up the amount of nodes or slides that are not in the right place :O
def misplaced(puz, goal):
    print('\nThis is the current puzzle:')
    print_puzzle(puz)

    #you need a counter, which is h(n)
    counter = 0

    #wanna compare two slides together
    #i is row, j is column
    for i in range(len(puz)):
        for j in range(len(puz)):
            #checks if the tile is the same
            #makes it into a int by int()
            #check when puzzle at row and column doesn't equal to goal puz at
            #row and column
            if(int(puz[i][j]) != goal[i][j] and int(puz[i][j] != 0)) :
                counter +=1
    print('The h(n) is ' + str(counter) + '\n')

    return counter    

#want to print the puzzle pretty
def print_puzzle(puz):
    # i is row

    for i in range(len(puz)):
        print('|', end = "")
        
        for j in range(len(puz)):
            if( j != len(puz)-1):
                print(puz[i][j], end ="," )
            else:
                print(puz[i][j], end ="|\n")


#will be further implemented for other types of 8puzzle
def check_puzzle(puz):
    check = True
    for i in range(len(puz)):        
        for j in range(len(puz)):
            if puz[i][j] == '1' or puz[i][j] == '2' or puz[i][j] == '3' or puz[i][j] == '4' or puz[i][j] == '5' or puz[i][j] == '6' or puz[i][j] == '7' or puz[i][j] == '8' or puz[i][j] == '0' :
                check = True
            else:
                check = False
    if check == False:
        print('ERROR: insert a number between 1-8, use 0 to indicate an empty tile.\n')
        main()

#way to check if it's a goal
def is_it_goal(puz,goal):
    output = True

    print('Is it goal?\nCurrent puzzle:')
    print_puzzle(puz)


    for i in range(len(puz)):
        for j in range(len(puz)):
            if(int(puz[i][j]) != goal[i][j]):
                output = False
                return output
            else:
                output = True
                
    return output

#https://www.codecademy.com/learn/learn-data-structures-and-algorithms-with-python/modules/nodes/cheatsheet
class node:
    def __init__(self, puzzle):
        #initialize
        self.puzzle = puzzle
        self.cost = 0
        self.depth = 0
        self.nleft = None
        self.nright = None
        self.nup = None
        self.ndown = None
        self.expanded = False

#runs main
if __name__ == "__main__":
    main()