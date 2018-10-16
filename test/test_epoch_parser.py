import unittest
import sys

from src.epoch_parser import EpochParser

sys.path.append('../src')


class TestStringMethods(unittest.TestCase):

    def test_weird_bug(self):
        self.assertEqual('1970-01-02T01:00:01', EpochParser.parse('0').isoformat())
        self.assertEqual('1970-01-02T01:00:01', EpochParser.parse('86400').isoformat())

    def test_min_timestamp(self):
        self.assertEqual('1970-01-02T01:00:01', EpochParser.parse('86401').isoformat())

    def test_timestamp(self):
        self.assertEqual('2018-10-06T21:23:33', EpochParser.parse('1538853813').isoformat())

    def test_random_string(self):
        self.assertIsNone(EpochParser.parse('abc'))


if __name__ == '__main__':
    unittest.main()
