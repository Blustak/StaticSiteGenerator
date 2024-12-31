import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_constructor(self):
        node = ParentNode(None, None)
        for v in (node.tag, node.value, node.children, node.props):
            self.assertEqual(v, None)

        t_children = [
            LeafNode("p", "hey ya", {"artist": "Andre3000 (ice cold)"}),
            LeafNode("span", "this was fun!"),
        ]
        t_props = {"href": "yahoo.co.jp"}
        node_with_vals = ParentNode(
            "p",
            t_children,
            props=t_props,
        )
        self.assertEqual(node_with_vals.tag, "p")
        self.assertEqual(node_with_vals.children, t_children)
        self.assertEqual(node_with_vals.props, t_props)
        self.assertIsNone(node_with_vals.value)

    def test_to_html_empty(self):
        node = ParentNode("div", [])
        node_expected = "<div></div>"
        self.assertEqual(node.to_html(), node_expected)
        node_props = ParentNode(
            "div",
            [],
            {
                "href": "google.ur.mom",
                "style": "too_cool_for_school;",
            },
        )
        node_props_expected = (
            '<div href="google.ur.mom" style="too_cool_for_school;"></div>'
        )
        self.assertEqual(node_props_expected, node_props.to_html())

    def test_to_html_1d(self):
        children = [
            LeafNode("p", "hello"),
            LeafNode("p", "world", {"style": "colour:bluey;"}),
        ]
        node = ParentNode("div", children)
        node_expected = (
            "<div>"
            + "<p>hello</p>"
            + '<p style="colour:bluey;">'
            + "world</p>"
            + "</div>"
        )

        self.assertEqual(node_expected, node.to_html())

    def test_to_html_nested(self):
        child_list_1 = [
            LeafNode("p", "hello"),
            LeafNode("p", "world", {"style": "colour:bluey;"}),
        ]
        child_list_2 = [
            LeafNode("a", "google", {"href": "google.com"}),
            LeafNode("i", "tee hee", {
                     "style": "size:1000pt;", "class": "bigBoi"}),
        ]
        parent_node_1 = ParentNode("div", child_list_1)
        nested_list = [
            LeafNode("p", "nesting!", {"layout": "flex"}),
            ParentNode("div", child_list_2),
            parent_node_1,
        ]
        node = ParentNode("div", nested_list)
        expected = (
            "<div>"
            + '<p layout="flex">'
            + "nesting!"
            + "</p>"
            + "<div>"
            + '<a href="google.com">'
            + "google"
            + "</a>"
            + '<i style="size:1000pt;" class="bigBoi">'
            + "tee hee"
            + "</i>"
            + "</div>"
            + "<div>"
            + "<p>hello</p>"
            + '<p style="colour:bluey;">'
            + "world"
            + "</p>"
            + "</div>"
            + "</div>"
        )
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
