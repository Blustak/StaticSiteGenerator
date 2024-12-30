import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
