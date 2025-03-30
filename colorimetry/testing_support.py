import unittest


class TestBase(unittest.TestCase):
    maxDiff = None

    def assertEquals(self, a, b):
        return self.assertEqual(a, b)
