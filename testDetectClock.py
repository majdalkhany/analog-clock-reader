import unittest
from detectClock import detectClock

class TestDetectClock(unittest.TestCase):
    def testDetectClock(self):
        self.assertEqual("3:07:03", detectClock("clock1.jpg"))
        self.assertEqual("3:07:03", detectClock("clock1_skew.jpg"))
        # self.assertEqual("10:09:25", detectClock("clock2.jpg"))
        # self.assertEqual("5:59:22", detectClock("clock3.jpg"))
        # self.assertEqual("10:09:38", detectClock("clock4.jpg"))
        # self.assertEqual("10:10:34", detectClock("watch1.jpg"))
unittest.main()