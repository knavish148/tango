import unittest
from toyrobot import *

class TestToyRobot(unittest.TestCase):

    # testdata containing incorrect prog_args
    wrongArgs = [
        ['GENJI', 'INEEDHEALING'],
        ['PLACE', 'MOVE', 'LEFT'],
        ['3,4,EAST', 'LEFT', 'MOVE', 'REPORT'],
        ['PLACE', '0,0,SOUTH', 'MOVR'],
        ['PLACE', '4,4,SOUTH', 'MOVE', 'LINKS', 'REPORT'],
        ['PLACE', '4,2,SOUTH', 'MOVE', 'LINKS', 'REPORT'],
        ['PLACE', '2,2,NORTH', 'MOVE', 'RIGHT', 'REPORTED'],
        ['PLACE', '4,4,SOUTH', 'left']
    ],

    # testdata in form of (prog_args, expectedPosition, expectedPlaced)
    robotPlacingAndMoving = [
        # testdata set for robot placing
        (['PLACE', '0,0,SOUTHWEST'],
         {}, False),
        (['PLACE', '0,0,KANYE', 'PLACE', '4,1,NORTHWEST'],
         {}, False),
        (['PLACE', '4,5,SOUTH', 'PLACE', '123,0,NORTH', 'PLACE', '3,3,EAST'],
         {'X': 3, 'Y': 3, 'F': 'EAST'}, True),
        (['PLACE', '1,4,NORTH'],
         {'X': 1, 'Y': 4, 'F': 'NORTH'}, True),
        (['LEFT', 'RIGHT', 'PLACE', '1,5,NORTH', 'LEFT', 'PLACE', '1,4,NORTH'],
         {'X': 1, 'Y': 4, 'F': 'NORTH'}, True),
        # test multiple placing
        (['PLACE', '4,4,NORTH', 'PLACE', '1,3,WEST'],
         {'X': 1, 'Y': 3, 'F': 'WEST'}, True),
        (['PLACE', '0,0,SOUTH', 'LEFT', 'MOVE', 'REPORT', 'PLACE', '1,4,NORTH'],
         {'X': 1, 'Y': 4, 'F': 'NORTH'}, True),
        # testdata set for requirement of robot not performing dangerous moves
        (['PLACE', '0,0,SOUTH', 'MOVE'],
         {'X': 0, 'Y': 0, 'F': 'SOUTH'}, True),
        (['PLACE', '4,4,SOUTH', 'LEFT', 'MOVE'],
         {'X': 4, 'Y': 4, 'F': 'EAST'}, True),
        (['PLACE', '0,0,SOUTH', 'MOVE'],
         {'X': 0, 'Y': 0, 'F': 'SOUTH'}, True),
        (['PLACE', '1,1,WEST', 'RIGHT', 'RIGHT', 'MOVE', 'RIGHT', 'MOVE', 'MOVE'],
         {'X': 2, 'Y': 0, 'F': 'SOUTH'}, True),
        # test multiple robot moves
        (['PLACE', '2,2,SOUTH', 'LEFT', 'LEFT', 'LEFT', 'LEFT'],
         {'X': 2, 'Y': 2, 'F': 'SOUTH'}, True),
        (['PLACE', '4,0,WEST', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'LEFT', 'REPORT'],
         {'X': 0, 'Y': 0, 'F': 'SOUTH'}, True),
        (['PLACE', '4,0,WEST', 'MOVE', 'MOVE', 'PLACE', '3,4,EAST', 'MOVE', 'REPORT'],
         {'X': 4, 'Y': 4, 'F': 'EAST'}, True),
        (['PLACE', '5,5,SOUTH', 'REPORT', 'MOVE', 'PLACE', '3,3,WEST', 'RIGHT', 'MOVE', 'RIGHT', 'REPORT'],
         {'X': 3, 'Y': 4, 'F': 'EAST'}, True),
        (['PLACE', '4,4,EAST', 'MOVE', 'RIGHT', 'MOVE', 'MOVE', 'LEFT', 'MOVE'],
         {'X': 4, 'Y': 2, 'F': 'EAST'}, True)
    ]

    # check data has initial value before every test
    def setUp(self):
        self.assertEqual(getPosition(), {})
        self.assertEqual(getRobotPlaced(), False)

    # set global variables to inital state to be safe
    def tearDown(self):
        setRobotPlaced(False)
        setPosition({})

    # test program called with wrong program arguments
    def test_wrongArgs(self):
        for arg in self.wrongArgs:

            with self.assertRaises(SystemExit) as cm:
                toyrobot(arg)
            self.assertEqual(cm.exception.code, 2)

            self.assertEqual(getPosition(), {})
            self.assertEqual(getRobotPlaced(), False)

    # test robot placement on the tabletop
    def test_robotPlacingAndMoving(self):
        for (arg, expectedPos, expectedPlaced) in self.robotPlacingAndMoving:
            with self.assertRaises(SystemExit) as cm:
                toyrobot(arg)
            self.assertEqual(cm.exception.code, 0)

            self.assertEqual(getPosition(), expectedPos)
            self.assertEqual(getRobotPlaced(), expectedPlaced)

            setPosition({})
            setRobotPlaced(False)


# run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestToyRobot)
unittest.TextTestRunner(verbosity=2).run(suite)