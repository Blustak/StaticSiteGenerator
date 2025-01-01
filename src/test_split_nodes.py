import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextType, TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(split_nodes_delimiter([], None, TextType.TEXT), [])

    def test_single(self):
        node = TextNode("foo", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.TEXT)
        self.assertEqual([node], new_nodes)

    def test_single_bold(self):
        node = TextNode("foo**bar**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("foo", TextType.TEXT),
                    TextNode("bar", TextType.BOLD)]
        self.assertListEqual(expected, new_nodes)

    def test_single_italic(self):
        node = TextNode("foo*bar*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [TextNode("foo", TextType.TEXT),
                    TextNode("bar", TextType.ITALIC)]
        self.assertListEqual(expected, new_nodes)

    def test_single_code(self):
        node = TextNode("foo`bar`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("foo", TextType.TEXT),
                    TextNode("bar", TextType.CODE)]
        self.assertListEqual(expected, new_nodes)

    def test_single_multi(self):
        node = TextNode(
            "This is a *long* line of `decorators`"
            + " such that **things** need to be *handled with care*",
            TextType.TEXT,
        )

        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("long", TextType.ITALIC),
            TextNode(" line of ", TextType.TEXT),
            TextNode("decorators", TextType.CODE),
            TextNode(" such that ", TextType.TEXT),
            TextNode("things", TextType.BOLD),
            TextNode(" need to be ", TextType.TEXT),
            TextNode("handled with care", TextType.ITALIC),
        ]

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

        self.assertListEqual(new_nodes, expected)
