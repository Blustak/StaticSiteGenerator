import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode()
        self.assertTrue(
            node.tag is None
            and node.value is None
            and node.children is None
            and node.props is None
        )

    def test_constructor_with_values(self):
        tag = "p"
        value = "Lorem Ipsum"
        children = [HTMLNode(), HTMLNode()]
        props = {
            "href": "https://www.google.com",
        }

        node = HTMLNode(tag, value, children, props)
        self.assertTrue(
            node.tag is tag
            and node.value is value
            and node.children is children
            and node.props is props
        )

    def test_props_to_html_single(self):
        props = {
            "href": "https://www.google.com",
        }
        node = HTMLNode(props=props)
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
            f"Error in {node}",
        )

    def test_props_to_html_multi(self):
        props = {
            "href": "https://www.google.com",
            "style": "color:rgba(0,0,0,0);\nfont:comic sans",
            "id": "large_div",
            "class": "smol_div",
            "alternate": "very nice div",
        }
        node = HTMLNode(tag="div", props=props)
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"'
            + ' style="color:rgba(0,0,0,0);\nfont:comic sans"'
            + ' id="large_div" class="smol_div" alternate="very nice div"',
        )


class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        node = LeafNode("p", "Lorum Ipsum")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Lorum Ipsum")
        self.assertIsNone(node.children)

    def test_to_html(self):
        node = LeafNode("p", "Lorum Ipsum")
        self.assertEqual(
            node.to_html(),
            "<p>Lorum Ipsum</p>",
            f"Error with node {node}",
        )
        node_with_props = LeafNode(
            "p",
            "Lorum Ipsum",
            {"href": "google.com", "id": "coolio"},
        )
        self.assertEqual(
            node_with_props.to_html(),
            '<p href="google.com" id="coolio">Lorum Ipsum</p>',
            f"Error with node:{node_with_props}",
        )


if __name__ == "__main__":
    unittest.main()
