import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(split_nodes_delimiter([], None, TextType.TEXT), [])
