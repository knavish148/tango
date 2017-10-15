import sys, argparse, re

# global vars
position = {}
robotPlaced = False

# main program function
# argv: command line arguments
def toyrobot(argv):
    idx = 0

    # parse program arguments
    while idx != len(argv):
        arg = argv[idx]

        if (arg == 'PLACE'):
            try:
                placeRobot(argv[idx + 1])
                idx += 1
            except IndexError:
                print 'Incorrect PLACE argument'
                sys.exit(2)
        elif ((arg == 'LEFT') | (arg == 'RIGHT')):
            if robotPlaced:
                setFacingSide(arg)
        elif (arg == 'MOVE'):
            if robotPlaced:
                updatePosition()
        elif (arg == 'REPORT'):
            if robotPlaced:
                reportPosition()
        else:
            print("Wrong program argument!")
            sys.exit(2)

        idx += 1

    sys.exit(0)

# place robot on the tabletop
# positionArg: command line argument of format X,Y,F
def placeRobot(positionArg):
    global position
    global robotPlaced

    # Use regex to check if robot is placed correctly
    matchObj = re.match('([0-4])\,([0-4])\,(NORTH|SOUTH|EAST|WEST)$', positionArg)
    if matchObj:
        try:
            position = {'X': int(matchObj.group(1)),
                        'Y': int(matchObj.group(2)),
                        'F': matchObj.group(3)}
            robotPlaced = True
        except ValueError:
            print 'Position must be of type int'

# determine which side robot will be facing based on left or right input
# side: LEFT or RIGHT
def setFacingSide(side):
    global position

    # All possible transitions
    # initial face + side = resulting face
    transitions = [('NORTH', 'LEFT',  'WEST'),
                   ('NORTH', 'RIGHT', 'EAST'),
                   ('SOUTH', 'LEFT',  'EAST'),
                   ('SOUTH', 'RIGHT', 'WEST'),
                   ('EAST',  'LEFT',  'NORTH'),
                   ('EAST',  'RIGHT', 'SOUTH'),
                   ('WEST',  'LEFT',  'SOUTH'),
                   ('WEST',  'RIGHT', 'NORTH')]

    [res] = [t for t in transitions if (t[0] == position['F']) & (t[1] == side)]
    position['F'] = res[2]

# update position of the robot based on current position and facing side
def updatePosition():
    global position
    xNew = position['X']
    yNew = position['Y']

    # calculate new X or Y based on facing side
    if position['F'] == 'NORTH':
        yNew += 1
    elif position['F'] == 'SOUTH':
        yNew -= 1
    elif position['F'] == 'EAST':
        xNew += 1
    else:
        xNew -= 1

    # update if new position is valid, ignore move otherwise
    if (0 <= xNew < 5) & (0 <= yNew < 5):
        position['X'] = xNew
        position['Y'] = yNew
    else:
        print 'Invalid new position ({},{})'.format(xNew, yNew)

# print robot position
def reportPosition():
    print('{},{},{}'.format(position['X'], position['Y'], position['F']))

# helper functions for UT

def getPosition():
    return position

def getRobotPlaced():
    return robotPlaced

def setPosition(newPosition):
    global position
    position = newPosition

def setRobotPlaced(newRobotPlaced):
    global robotPlaced
    robotPlaced = newRobotPlaced


# program entry point
if __name__ == "__main__":
   toyrobot(sys.argv[1:])
