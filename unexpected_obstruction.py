"""
this program models a robot vacuum cleaner moving through a room 
represented as a grid, where each grid is either clean (True), 
dirty (False), or blocked by walls ('w') or a cat ('c')

the vacuum is also able to:
- move in 8 directions (N, NE, E, SE, S, SW, W, NW)
- turn left or right
- move forward (unless being blocked by something)
- push cats ahead by one tile if unblocked
- clean dirty tiles

the program will update and print the grid after each command the robot receives
"""

# the cleaning space grid (True = clean, False = dirty)
cleaning_space = [
    [True, True, True, True, True, True, True],
    [True, False, True, True, True, True, True], 
    [False, True, False, True, True, True, False], 
    [True, True, True, False, True, True, True], 
    [True, True, True, True, True, True, True], 
    [True, True, True, True, True, True, False]
    ]

# the obstruction space grid (None = empty, 'w' = wall, 'c' = cat, 'r' = robot)
obstruction_space = [
    [None, None, None, None, 'w', None, 'w'],
    [None, None, None, None, None, 'w', None], 
    [None, None, None, 'w', None, None, None], 
    [None, None, 'w', None, None, None, None], 
    [None, None, None, None, None, None, None], 
    [None, None, 'w', 'w', None, None, None]
    ]

# obstruction_space = [
#     [None,None,None,None,None,None,None,None,None,None],
#     [None,None,None,None,"c" ,None,None,None,None,None],
#     [None,None,"r" ,None,None,None,None,None,None,None],
#     [None,None,None,None,None,None,"w" ,None,None,None],
#     [None,None,None,None,None,None,None,None,None,None],
#     [None,"w" ,None,None,None,None,None,None,None,None],
#     [None,None,None,None,None,None,None,None,None,None],
#     [None,None,None,None,None,None,None,None,None,None],
#     [None,None,None,None,None,None,None,None,None,None],
#     [None,None,None,None,None,None,None,None,None,None],
#     ]

# cleaning_space = [
#     [True, True, True],
#     [True, True, True],
#     [True, True, True]
# ]

# obstruction_space = [
#     [None, "c", None],
#     [None, None, None],
#     [None, None, None]
# ]

def validate_bounds(n_row,n_col):
    """
    checks if the given position is within the cleanup area

    args:
    - n_row (int): row number to check
    - n_col (int): column number to check

    returns:
   -  bool: True if the position is valid, False if it is out of bounds
    """
    global cleaning_space
    
    return n_row < len(cleaning_space) and n_col < len(cleaning_space[0]) and n_row >= 0 and n_col >= 0

def get_new_position(n_row, n_col, robot_dir):
    """
    calculate where the robot will move next based on its current direction

    args:
    - row (int): the robot's current row
    - col (int): the robot's current column
    - direction (str): the direction it's facing

    returns:
    - tuple: the updated row / col position after moving one step
    """
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
    return n_row, n_col

def vacuum_action(vacuum, action):
    """
    makes the robot perform an action like move, turn, or clean

    args:
    - vacuum (list): the current state of the robot as [row, column, direction]
    - action (str): the option robot should do ('turn left', 'turn right', 'clean', 'forward'

    result:
    -  str: the actual action the robot ended performing
    """
    global cleaning_space
    global obstruction_space

    robot_row, robot_col, robot_dir = vacuum
    n_row, n_col = robot_row, robot_col

    # list of possible directions
    all_dir = ["N","NE","E","SE","S","SW","W","NW"]

    final_action = ""

    # process the action (turn-left, turn-right, clean, forward)
    match action:
        # turn the robot 90 degrees left from its current direction
        case "turn-left":
            robot_dir = all_dir[((all_dir.index(robot_dir)-1) % len(all_dir))]
            final_action = action
        # turn the robot 90 degrees right from its current direction
        case "turn-right":
            robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
            final_action = action
        # clean the current tile
        case "clean":
            if(cleaning_space[robot_row][robot_col] == True):
                for i in range (len(obstruction_space)):
                  for j in range (len(obstruction_space[i])):
                    if obstruction_space[i][j] == "r":
                        obstruction_space[i][j] = None

            cleaning_space[robot_row][robot_col] = True
            final_action = action
        #move forward
        case "forward":
            n_row, n_col = get_new_position(n_row, n_col, robot_dir)
            if validate_bounds(n_row, n_col):
              match obstruction_space[n_row][n_col]:
                  # if a cat is in the way, move the cat ahead and turn right
                  case "c":
                    cat_row, cat_col = get_new_position(n_row, n_col, robot_dir)
                    if (validate_bounds(cat_row, cat_col) and obstruction_space[cat_row][cat_col] == None):
                      obstruction_space[n_row][n_col] = None
                      obstruction_space[cat_row][cat_col] = "c"
                      
                    robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                    final_action = "turn-right"
                        
                  # if there's a wall, turn right
                  case "w":
                    robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                    final_action = "turn-right"
                 # proceed to move if new position is clear  
                  case None:
                    if (cleaning_space[robot_row][robot_col] == False):
                      cleaning_space[n_row][n_col] = False
                    robot_row, robot_col = n_row,n_col
                    final_action = "forward"
            else:
                # if the move goes out of bounds, turn right
                robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                final_action = "turn-right"

    # update the vacuum position and direction after the action
    vacuum[0] = robot_row
    vacuum[1] = robot_col
    vacuum[2] = robot_dir

    print((vacuum))
    for i in range (len(obstruction_space)):
      for j in range (len(obstruction_space[i])):
        if obstruction_space[i][j] == "r":
            obstruction_space[i][j] = None

    obstruction_space[robot_row][robot_col] = "r"

    # print(cleaning_space)
    # print(obstruction_space)
    return final_action

def perform_cleaning(instructions, vacuum, log):
    """
    reads instructions from a file, 
    moves the robot step by step, and keeps track of each move
    
    args:
    - instructions (str): path to a text file with commands for the robot
    - vacuum (list): the robot's starting position and direction in [row, column, direction] format
    - log (str): file path to write the robot's actual actions
    """
    open(log, 'w').close()

    f = open(instructions, "r")
    fl = open(log, 'a')

    idx = 1
    for line in f.readlines():
        print("PROCESS ", idx)
        for row_index,row in enumerate(cleaning_space):
          for col_index,cell in enumerate(row):
              if obstruction_space[row_index][col_index] is not None:
                  print(obstruction_space[row_index][col_index],end='')
              elif (row_index,col_index) == (vacuum[0],vacuum[1]):
                  print("r",end='')
              elif cell:
                  print(".",end='')
              else:
                  print(".",end='')
          print()
        idx += 1
        perform = vacuum_action(vacuum, line.strip())  
        fl.write(perform + '\n')

    f.close()
    fl.close()

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    """
    main function to simulate the robot's action
    - sets initial vacuum state
    - loads command file
    - runs simulation
    - prints the state of the space before and after cleaning
    - shows the action log
    """
    test_commands = "test_commands.txt"
    test_log = "test_log.txt"
    vacuum = [4, 4, 'SE']

    print("INITIAL SPACE")
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index],end='')
            elif (row_index,col_index) == (vacuum[0],vacuum[1]):
                print("r",end='')
            elif cell:
                print(".",end='')
            else:
                print(".",end='')
        print()

    # print("CLEANING")
    perform_cleaning(test_commands,vacuum,test_log)

    print("FINAL SPACE")
    # print the final state of the grid after cleaning
    for row_index,row in enumerate(cleaning_space):
        for col_index,cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index],end='')
            elif (row_index,col_index) == (vacuum[0],vacuum[1]):
                print("r",end='')
            elif cell:
                print(".",end='')
            else:
                print(".",end='')
        print()

    # print the action log
    print("ACTIONS")
    with open(test_log,"r") as log:
        print(log.read())
