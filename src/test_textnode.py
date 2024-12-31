import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode(
            "This is a text node that is different", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,
                         "some/path/to/something")
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("I am a text node!", TextType.TEXT)
        node = text_node_to_html_node(text_node)
        expected = "I am a text node!"
        self.assertEqual(node.to_html(), expected)

    def test_bold(self):
        value = "I am a bold node!"
        text_node = TextNode(value, TextType.BOLD)
        node = text_node_to_html_node(text_node)
        expected = f"<b>{value}</b>"
        self.assertEqual(node.to_html(), expected)

    def test_italic(self):
        value = "I am a italic node!"
        text_node = TextNode(value, TextType.ITALIC)
        node = text_node_to_html_node(text_node)
        expected = f"<i>{value}</i>"
        self.assertEqual(node.to_html(), expected)

    def test_code(self):
        value = "I am a code node!"
        text_node = TextNode(value, TextType.CODE)
        node = text_node_to_html_node(text_node)
        expected = f"<code>{value}</code>"
        self.assertEqual(node.to_html(), expected)

    def test_link(self):
        value = "I am a link node!"
        link = "google.com"
        text_node = TextNode(value, TextType.LINK, link)
        node = text_node_to_html_node(text_node)
        expected = f'<a href="{link}">{value}</a>'
        self.assertEqual(node.to_html(), expected)

    def test_image(self):
        value = "cool cat pic"
        link = "cat_pics.jpg"
        text_node = TextNode(value, TextType.IMAGE, link)
        node = text_node_to_html_node(text_node)
        expected = f'<img src="{link}" alt="{value}"></img>'
        self.assertEqual(node.to_html(), expected)

    def test_exceptions(self):
        text_node = TextNode(None, None)
        with self.assertRaises(Exception):
            _ = text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
