"""
Implementation of Toy Robot task

Program that places robot on the board, moves it over the board
and reports it's position.
"""
import sys
import re

# global vars
POSITION = {}
ROBOT_PLACED = False

def toy_robot(argv):
    """
    Main program function.

    :param position_arg: command line arguments
    :return: 0 if program succeds, 2 otherwise
    """
    idx = 0

    # parse program arguments
    while idx != len(argv):
        arg = argv[idx]

        if arg == 'PLACE':
            try:
                place_robot(argv[idx + 1])
                idx += 1
            except IndexError:
                print 'Incorrect PLACE argument'
                sys.exit(2)
        elif (arg == 'LEFT') | (arg == 'RIGHT'):
            if ROBOT_PLACED:
                set_facing_side(arg)
        elif arg == 'MOVE':
            if ROBOT_PLACED:
                update_position()
        elif arg == 'REPORT':
            if ROBOT_PLACED:
                report_position()
        else:
            print "Wrong program argument!"
            sys.exit(2)

        idx += 1

    sys.exit(0)

def place_robot(position_arg):
    """
    place robot on the tabletop

    :param position_arg: command line argument of format X,Y,F
    :return: -
    """
    global POSITION
    global ROBOT_PLACED

    # Use regex to check if robot is placed correctly
    match_obj = re.match('([0-4])\,([0-4])\,(NORTH|SOUTH|EAST|WEST)$', position_arg)
    if match_obj:
        try:
            POSITION = {'X': int(match_obj.group(1)),
                        'Y': int(match_obj.group(2)),
                        'F': match_obj.group(3)}
            ROBOT_PLACED = True
        except ValueError:
            print 'Position must be of type int'

def set_facing_side(side):
    """
    Determine which side robot will be facing based on left or right input

    :param side: LEFT or RIGHT
    :return: -
    """
    global POSITION

    # All possible transitions
    # initial face + side = resulting face
    transitions = [('NORTH', 'LEFT', 'WEST'),
                   ('NORTH', 'RIGHT', 'EAST'),
                   ('SOUTH', 'LEFT', 'EAST'),
                   ('SOUTH', 'RIGHT', 'WEST'),
                   ('EAST', 'LEFT', 'NORTH'),
                   ('EAST', 'RIGHT', 'SOUTH'),
                   ('WEST', 'LEFT', 'SOUTH'),
                   ('WEST', 'RIGHT', 'NORTH')]

    [res] = [t for t in transitions if (t[0] == POSITION['F']) & (t[1] == side)]
    POSITION['F'] = res[2]

def update_position():
    """Update position of the robot based on current position
    and facing side"""
    global POSITION
    x_new = POSITION['X']
    y_new = POSITION['Y']

    # calculate new X or Y based on facing side
    if POSITION['F'] == 'NORTH':
        y_new += 1
    elif POSITION['F'] == 'SOUTH':
        y_new -= 1
    elif POSITION['F'] == 'EAST':
        x_new += 1
    else:
        x_new -= 1

    # update if new position is valid, ignore move otherwise
    if (0 <= x_new < 5) & (0 <= y_new < 5):
        POSITION['X'] = x_new
        POSITION['Y'] = y_new
    else:
        print 'Invalid new position ({},{})'.format(x_new, y_new)

def report_position():
    """print robot position"""
    print '{},{},{}'.format(POSITION['X'], POSITION['Y'], POSITION['F'])

def get_position():
    """UT helper. Gets global POSITION value"""
    return POSITION

def get_robot_placed():
    """UT helper. Gets global ROBOT_PLACED value"""
    return ROBOT_PLACED

def set_position(new_position):
    """UT helper. Sets global POSITION value"""
    global POSITION
    POSITION = new_position

def set_robot_placed(new_robot_placed):
    """UT helper. Sets global ROBOT_PLACED value"""
    global ROBOT_PLACED
    ROBOT_PLACED = new_robot_placed


# program entry point
if __name__ == "__main__":
    toy_robot(sys.argv[1:])
