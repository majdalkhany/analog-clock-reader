import unittest
from detectClock import detectClock

class TestDetectClock(unittest.TestCase):
    def testDetectClock(self):
        self.assertEqual("3:07:03", detectClock("clock1.jpg"))

unittest.main()