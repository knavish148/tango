"""Unit test suite for Toy Robot"""

import unittest
import toyrobot

class TestToyRobot(unittest.TestCase):
    """Test class for Toy Robot program"""

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
        (['PLACE', '5,5,SOUTH', 'REPORT', 'MOVE', 'PLACE', '3,3,WEST',
          'RIGHT', 'MOVE', 'RIGHT', 'REPORT'],
         {'X': 3, 'Y': 4, 'F': 'EAST'}, True),
        (['PLACE', '4,4,EAST', 'MOVE', 'RIGHT', 'MOVE', 'MOVE', 'LEFT', 'MOVE'],
         {'X': 4, 'Y': 2, 'F': 'EAST'}, True)
    ]

    def setUp(self):
        """check data has initial value before every test"""
        self.assertEqual(toyrobot.get_position(), {})
        self.assertEqual(toyrobot.get_robot_placed(), False)

    def tearDown(self):
        """set global variables to inital state to be safe"""
        toyrobot.set_robot_placed(False)
        toyrobot.set_position({})

    def test_wrong_args(self):
        """test program called with wrong program arguments"""
        for arg in self.wrongArgs:

            with self.assertRaises(SystemExit) as e:
                toyrobot.toy_robot(arg)
            self.assertEqual(e.exception.code, 2)

            self.assertEqual(toyrobot.get_position(), {})
            self.assertEqual(toyrobot.get_robot_placed(), False)

    def test_robot_placing_and_moving(self):
        """test robot placement on the tabletop"""
        for (arg, expected_pos, expected_placed) in self.robotPlacingAndMoving:
            with self.assertRaises(SystemExit) as e:
                toyrobot.toy_robot(arg)
            self.assertEqual(e.exception.code, 0)

            self.assertEqual(toyrobot.get_position(), expected_pos)
            self.assertEqual(toyrobot.get_robot_placed(), expected_placed)

            toyrobot.set_position({})
            toyrobot.set_robot_placed(False)


# run the tests
SUITE = unittest.TestLoader().loadTestsFromTestCase(TestToyRobot)
unittest.TextTestRunner(verbosity=2).run(SUITE)
