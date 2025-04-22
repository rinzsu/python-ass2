"""
this program simulates a robot vacuum cleaner moving through a room 
represented as a grid, where each grid is either clean (None), dirty ('d'), water ('l'), 
mud ('m'), soap ('s'), blocked by walls ('w') or cats ('c')

the vacuum performs several actions, such as:
- 'turn left': turns the vacuum cleaner 90 degrees to the left
- 'turn right': turns the vacuum cleaner 90 degrees to the right
- 'clean': cleans the current tile if it contains dirt
- 'mop': mops the air to turn it into soap
- 'forward': moves the vacuum cleaner one step in the current direction

behavior for moving forward:
- if on the ground ('d'): the vacuum cleaner smears dirt to a new location
- if in the water ('l'): the vacuum slips and moves two steps forward, spreading water over the skipped locations
- if in soap ('s'): the vacuum slips and moves two steps forward, setting the location passed to clean ('None')
- if in mud ('m'): the vacuum cleaner smears mud to a new location
- if the vacuum cleaner tries to move out of bounds or obstacles: it turns right

special rules:
- if the vacuum hits a cat, the cat moves one step in the vacuum's direction, provided the space is clear
- the vacuum can't go through walls and will turn right instead
- if the vacuum faces another robot, it turns left instead of moving forward
"""

# initial grid: cleaning status
cleaning_space = [
   [None, None, 'd', None, None], 
   [None, None, None, None, None], 
   ['l', None, None, None, None], 
   ['d', None, None, None, None], 
   [None, None, None, None, None], 
   [None, None, None, 'l', None]] 

# initial grid: obstruction status
obstruction_space = [
   [None, None, 'r', None, None], 
   [None, 'w', None, None, None], 
   [None, None, None, None, None], 
   [None, None, None, None, None], 
   ['w', None, None, None, None], 
   [None, None, None, None, None]]

def validate_bounds(n_row, n_col):
    """
    checks if the given position is within the cleanup area

    args:
    - n_row (int): row number to check
    - n_col (int): column number to check

    returns:
    - bool: True if the position is valid, False if it is out of bounds
    """
    global cleaning_space
    return n_row < len(cleaning_space) and n_col < len(cleaning_space[0]) and n_row >= 0 and n_col >= 0

def get_new_position(n_row, n_col, robot_dir):
    """
    calculate the new position of the robot based on direction

    args:
    - n_row, n_col (int): current coordinates
    - robot_dir (str): one of "N", "NE", ..., "NW"

    returns:
    - tuple: new (row, col) after moving one step in direction
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
    - vacuum (list): robot state [row, col, direction]
    - action (str): action to perform ("turn-left", "turn-right", "forward", "clean")

    returns:
    - str: the final action taken (may change due to obstacles)
    """
    global cleaning_space
    global obstruction_space

    robot_row, robot_col, robot_dir = vacuum
    obstruction_space[robot_row][robot_col] = None  # temporarily remove robot from current cell
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
            match (cleaning_space[robot_row][robot_col]):
                case True:
                    # full cleaning: remove robot from all spots
                    for i in range (len(obstruction_space)):
                        for j in range (len(obstruction_space[i])):
                            if obstruction_space[i][j] == "r":
                                obstruction_space[i][j] = None
                    cleaning_space[robot_row][robot_col] = None
                case "l":
                    cleaning_space[robot_row][robot_col] = "l"
                case "d":
                    cleaning_space[robot_row][robot_col] = None
            final_action = action
        # move forward
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
                        # if blocked, turn right
                        robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                        final_action = "turn-right"
                    # if there's a wall, turn right
                    case "w":
                        robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                        final_action = "turn-right"
                    
                    # if encounteres another robot, turn left
                    case "r":
                        robot_dir = all_dir[((all_dir.index(robot_dir)-1) % len(all_dir))]
                        final_action = "turn-left"
                    case None:
                        match (cleaning_space[robot_row][robot_col]):
                            case "d":
                                match cleaning_space[n_row][n_col]: 
                                    case None:
                                        cleaning_space[n_row][n_col] = "d"
                                    case "l":
                                        cleaning_space[n_row][n_col] = "m"
                            case "l":
                                # the vacuum is on water, slips and moves 2 positions
                                old_row, old_col = n_row, n_col
                                n_row, n_col = get_new_position(n_row, n_col, robot_dir)
                                if not validate_bounds(n_row, n_col):
                                    robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                                    final_action = "turn-right"
                                    vacuum[0] = robot_row
                                    vacuum[1] = robot_col
                                    vacuum[2] = robot_dir
                                    return final_action
                                else: 
                                    match (cleaning_space[n_row][n_col]):
                                        case None:
                                            cleaning_space[old_row][old_col] = "l"
                                        case "d": 
                                            cleaning_space[old_row][old_col] = "m"
                                        case "l":
                                            cleaning_space[old_row][old_col] = "l"
                            # if vacuum is on mud, spread mud to the nexr tile
                            case "m":
                                cleaning_space[n_row][n_col] = "m"
                        robot_row, robot_col = n_row, n_col
                        final_action = "forward"
            else:
                # move invalid, turn right
                robot_dir = all_dir[((all_dir.index(robot_dir)+1) % len(all_dir))]
                final_action = "turn-right"

    # update vacuum state and place robot again
    vacuum[0] = robot_row
    vacuum[1] = robot_col
    vacuum[2] = robot_dir
    obstruction_space[robot_row][robot_col] = "r"
    return final_action

def group_command_by_robot_no(command_file):
    """
    reads robot commands from a file and groups them by robot number

    args:
    - command_file (str): path to command file

    returns:
    - dict: keys are robot numbers, values are list of commands
    """
    command = {}
    f = open(command_file, "r")
    for line in f.readlines():
        command_split = line.split()
        robot_no, robot_commands = int(command_split[0]), command_split[1].split(",")

        if (robot_no in command):
            command[robot_no] += robot_commands
        else:
            command[robot_no] = robot_commands

    return command

def perform_cleaning(instructions, vacuums, logs):
    """
    execute robot movement from a command file and log each move

    args:
    - instructions (str): file path to instruction set
    - vacuums (list): list of vacuum states, one for each robot
    - logs (list): paths to log files for each robot
    """
    f = open(instructions, "r")
    idx = 1
    
    all_command = group_command_by_robot_no(instructions)

    for robot_no, arr_robot_commands in all_command.items():
        open(logs[robot_no], 'w').close()
        fl = open(logs[robot_no], 'a')

        for command in arr_robot_commands:
            print("THIS ONE FOR ROBOT NO:", robot_no)
            for row_index, row in enumerate(cleaning_space):
                for col_index, cell in enumerate(row):
                    if obstruction_space[row_index][col_index] is not None:
                        print(obstruction_space[row_index][col_index], end='')
                    elif (row_index, col_index) in vacuums:
                        print("r", end='')
                    elif cell:
                        print(".", end='')
                    else:
                        print(".", end='')
                print()
            idx += 1
            perform = vacuum_action(vacuums[robot_no], command.strip()) 

            fl.write(perform + '\n')
        fl.close()

    print(vacuums)

    f.close()

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    """
    main function to simulate the vacuum robot's actions:
    - sets initial vacuum position and direction
    - performs the cleaning process in the space
    - prints the state of the space before and after cleaning
    - shows the action logs from the cleaning process
    """
    test_commands = "test_commands.txt"
    test_logs = ["output.txt"]
    vacuum = [0, 2, 'SE']

    print("INITIAL SPACE")
    # loop through the grid to print the initial state of the cleaning space
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell is None:
                print(".", end='')
            else:
                print(cell, end='')
        print()

    print("CLEANING")
    vacuum_action(vacuum, action="clean")

    print("FINAL SPACE")
    # print the final state of the grid after cleaning
    for row_index, row in enumerate(cleaning_space):
        for col_index, cell in enumerate(row):
            if obstruction_space[row_index][col_index] is not None:
                print(obstruction_space[row_index][col_index], end='')
            elif cell is None:
                print(".", end='')
            else:
                print(cell, end='')
        print()

