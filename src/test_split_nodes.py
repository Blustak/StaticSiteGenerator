import unittest

from split_nodes import split_nodes_link, split_nodes_image
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
        expected = [
            TextNode("foo", TextType.TEXT),
            TextNode("bar", TextType.BOLD),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_single_italic(self):
        node = TextNode("foo*bar*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("foo", TextType.TEXT),
            TextNode("bar", TextType.ITALIC),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_single_code(self):
        node = TextNode("foo`bar`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("foo", TextType.TEXT),
            TextNode("bar", TextType.CODE),
        ]
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


class TestSplitNodesImageLink(unittest.TestCase):
    def test_single_image(self):
        text = (
            "a cool bit of text with image ![cat](www.cat.com/cat.jpg)"
            + " in the middle."
        )
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("a cool bit of text with image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "www.cat.com/cat.jpg"),
            TextNode(" in the middle.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_single_link(self):
        text = (
            "a cool bit of text with a link [cat](www.cat.com/cat.jpg)"
            + " in the middle."
        )
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("a cool bit of text with a link ", TextType.TEXT),
            TextNode("cat", TextType.LINK, "www.cat.com/cat.jpg"),
            TextNode(" in the middle.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_multiple_image(self):
        text = (
            "This is a test for ![image](imgur.com/foo.png)."
            + "It's a string with many ![sunglasses](www.coolcat.com/icon.img)"
            + " cool ![boiga](nyaccents.ny/delhi.jpg)"
            + "![awooga](./res/awooga.png)"
            + " images in it.![smiley](google.com/emoji.jpg)"
        )
        expected = [
            TextNode("This is a test for ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "imgur.com/foo.png"),
            TextNode(".It's a string with many ", TextType.TEXT),
            TextNode("sunglasses", TextType.IMAGE, "www.coolcat.com/icon.img"),
            TextNode(" cool ", TextType.TEXT),
            TextNode("boiga", TextType.IMAGE, "nyaccents.ny/delhi.jpg"),
            TextNode("awooga", TextType.IMAGE, "./res/awooga.png"),
            TextNode(" images in it.", TextType.TEXT),
            TextNode("smiley", TextType.IMAGE, "google.com/emoji.jpg"),
        ]

        node = TextNode(text, text_type=TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(expected, new_nodes)

    def test_multiple_link(self):
        text = (
            "This is a test for [image](imgur.com/foo.png)."
            + "It's a string with many [sunglasses](www.coolcat.com/icon.img)"
            + " cool [boiga](nyaccents.ny/delhi.jpg)"
            + "[awooga](./res/awooga.png)"
            + " links in it.[smiley](google.com/emoji.jpg)"
        )
        expected = [
            TextNode("This is a test for ", TextType.TEXT),
            TextNode("image", TextType.LINK, "imgur.com/foo.png"),
            TextNode(".It's a string with many ", TextType.TEXT),
            TextNode("sunglasses", TextType.LINK, "www.coolcat.com/icon.img"),
            TextNode(" cool ", TextType.TEXT),
            TextNode("boiga", TextType.LINK, "nyaccents.ny/delhi.jpg"),
            TextNode("awooga", TextType.LINK, "./res/awooga.png"),
            TextNode(" links in it.", TextType.TEXT),
            TextNode("smiley", TextType.LINK, "google.com/emoji.jpg"),
        ]

        node = TextNode(text, text_type=TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(expected, new_nodes)

    def test_multiple_combo(self):
        text = "\n".join(
            (
                "I am a long, complex string, with line breaks and",
                "all sorts in me. I have a ![few](pics.jpg)"
                + " bits of markdown sprinkled",
                "around, but some [are](malformed.",
                "So, let's [see](cool.com)"
                + " if this program ![can](tell.the) difference,",
                "and if ![both](functions)"
                + "[can](work)!"
                + "![in](tandem)[peace](boop)",
            )
        )
        text = text.strip()
        node = TextNode(text, TextType.TEXT)
        new_node_links = split_nodes_link([node])
        new_node_images = split_nodes_image([node])

        new_node_links_then_images = split_nodes_image(
            split_nodes_link(
                [
                    node,
                ]
            )
        )
        new_node_images_then_links = split_nodes_link(
            split_nodes_image(
                [
                    node,
                ]
            )
        )
        expected_links = [
            TextNode(
                "I am a long, complex string, with line breaks and"
                + "\nall sorts in me."
                + " I have a ![few](pics.jpg) bits of markdown sprinkled"
                + "\naround, but some [are](malformed."
                + "\nSo, let's ",
                TextType.TEXT,
            ),
            TextNode("see", TextType.LINK, "cool.com"),
            TextNode(
                " if this program ![can](tell.the) difference,"
                + "\nand if ![both](functions)",
                TextType.TEXT,
            ),
            TextNode("can", TextType.LINK, "work"),
            TextNode("!![in](tandem)", TextType.TEXT),
            TextNode("peace", TextType.LINK, "boop"),
        ]
        expected_images = [
            TextNode(
                "I am a long, complex string, with line breaks and"
                + "\nall sorts in me. I have a ",
                TextType.TEXT,
            ),
            TextNode("few", TextType.IMAGE, "pics.jpg"),
            TextNode(
                " bits of markdown sprinkled"
                + "\naround, but some [are](malformed."
                + "\nSo, let's [see](cool.com) if this program ",
                TextType.TEXT,
            ),
            TextNode("can", TextType.IMAGE, "tell.the"),
            TextNode(" difference,\nand if ", TextType.TEXT),
            TextNode("both", TextType.IMAGE, "functions"),
            TextNode("[can](work)!", TextType.TEXT),
            TextNode("in", TextType.IMAGE, "tandem"),
            TextNode("[peace](boop)", TextType.TEXT),
        ]
        expected_combo = [
            TextNode(
                "I am a long, complex string, with line breaks and"
                + "\nall sorts in me. I have a ",
                TextType.TEXT,
            ),
            TextNode("few", TextType.IMAGE, "pics.jpg"),
            TextNode(
                " bits of markdown sprinkled"
                + "\naround, but some [are](malformed."
                + "\nSo, let's ",
                TextType.TEXT,
            ),
            TextNode("see", TextType.LINK, "cool.com"),
            TextNode(" if this program ", TextType.TEXT),
            TextNode("can", TextType.IMAGE, "tell.the"),
            TextNode(" difference,\nand if ", TextType.TEXT),
            TextNode("both", TextType.IMAGE, "functions"),
            TextNode("can", TextType.LINK, "work"),
            TextNode("!", TextType.TEXT),
            TextNode("in", TextType.IMAGE, "tandem"),
            TextNode("peace", TextType.LINK, "boop"),
        ]
        self.assertListEqual(expected_links, new_node_links)
        self.assertListEqual(expected_images, new_node_images)
        self.assertListEqual(expected_combo, new_node_images_then_links)
        self.assertListEqual(expected_combo, new_node_links_then_images)
        # Both functions should get the same result.
        # Probably a useless operation, but better safe then sorry.
        self.assertListEqual(
            new_node_images_then_links,
            new_node_links_then_images,
        )
