"""
this program simulates a robot vacuum cleaning a grid-based space.
The space is represented by a grid of True (clean) and False (dirty) values, 
through which the vacuum moves, cleaning cells and updates its position based an instructions

the vacuum cleaner begins at a specific position and direction
and is capable of:
- rotating left or right,
- advancing in the current direction,
- cleaning its current position by moving it to the right (clean)
"""

# represents the grid with True for clean cells and False for dirty cells.
# cleaning_space = [ 
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,False,True,True,True,True,True,True,True],
#     #          ^^^^^
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,False,True,True,False,True,True,True,True],
#     #          ^^^^^           ^^^^^
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,True,True,False,True,True,True,True,True],
#     #                    ^^^^^
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,True,True,True,True,True,True,True,True],
#     [True,True,True,True,True,True,True,True,True,True]
#     ]

cleaning_space = [
    [True, True, True],
    [True, True, True],
    [True, True, True]
]

def validate_bounds(n_row,n_col):
    """
    check if the given position (row, column) is within the cleaning space limits.
    
    args:
    - n_row (int): target row index
    - n_col (int): target column index

    returns:
    - bool: True if within bounds, False otherwise    
    """
    global cleaning_space
    
    return n_row < len(cleaning_space) and n_col < len(cleaning_space[0]) and n_row >= 0 and n_col >= 0

def vacuum_action(vacuum, action):
    """
    execute an action (updating position and cleaning space on the robot vacum cleaner)

    args:
    - vacuum (list): [row, column, direction] representing the status of the vacuum cleaner
    - action (str): one of ['turn left', 'turn right', 'clean', 'forward']
    
    returns:
    - list: updated vacuum state after perform the action
    """
    global cleaning_space
    robot_row, robot_col, robot_dir = vacuum
    n_row, n_col = robot_row, robot_col

    #list all compass directions clockwise
    all_dir = ["N","NE","E","SE","S","SW","W","NW"]

    match action:
        case "turn-left":
            robot_dir = all_dir[((all_dir.index(robot_dir)-1) % len(all_dir))]
        case "turn-right":
            robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
        case "clean":
            cleaning_space[robot_row][robot_col] = True
        case "forward":
            match robot_dir:
                case "N":
                    n_row -= 1
                case "NE":
                    n_col += 1
                    n_row -= 1
                case "E":
                    n_col += 1
                case "SE":
                    n_col += 1
                    n_row += 1
                case "S":
                    n_row += 1
                case "SW":
                    n_col -= 1
                    n_row += 1
                case "W":
                    n_col -= 1
                case "NW":
                    n_row -= 1
                    n_col -= 1
            
            if validate_bounds(n_row, n_col):
                # update the robot's position if within bounds
                if (cleaning_space[robot_row][robot_col] == False):
                    cleaning_space[n_row][n_col] = False
                robot_row, robot_col = n_row,n_col
            else:
                # turn the robot to the right if it goes out of bounds
                robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
    
    vacuum[0] = robot_row
    vacuum[1] = robot_col
    vacuum[2] = robot_dir

def perform_cleaning(instructions, vacuum):
    """
    processes a list of processes from a file and applies it to vacuum

    args:
    instructions (str): path to a file containing one command per line
    vacuum (list): initial state of the rows, columns and vacuum directions
    """
    with open(instructions, "r") as f:
        for line in f:
            vacuum_action(vacuum, line.strip())

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    """
    main action to simulate the robot's action
    """
    test_commands = "test_commands.txt"
    vacuum = [1,1,"N"]

    print("INITIAL SPACE")
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if (row_index,col_index) == (vacuum[0],vacuum[1]):
                print("r",end='') # robot's position
            elif cell:
                print(".",end='') # clean cell
            else:
                print("d",end='') # dirty cell
        print()

    """
    the program displays the grid's initial and final states once all actions are completed   
    that includes:
    - "r": to show the vacuum's position  
    - ".": for clean spots
    - "d": for dirty spots
    """
    print("CLEANING")
    perform_cleaning(test_commands,vacuum)

    print("FINAL SPACE")
    # loop through the cleaning grid to display the final state
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if (row_index,col_index) == (vacuum[0],vacuum[1]):
                print("r",end='')
            elif cell:
                print(".",end='')
            else:
                print("d",end='')
        print()