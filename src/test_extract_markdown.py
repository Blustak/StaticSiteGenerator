import unittest

from extract_markdown import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_match(self):
        text = (
            "a bit of text with a single cat image."
            + " ![cool cat](www.cat_pics.org/cool_cat.gif)"
        )
        matches = extract_markdown_images(text)
        expected = [("cool cat", "www.cat_pics.org/cool_cat.gif")]
        self.assertListEqual(matches, expected)

    def test_multi_match(self):
        text = """
        a bit of text with multiple cat images,
        and stuff spread over a couple lines.
        ![cat licking its paw](www.cats.com/paw_licker.jpg)
        ![cat eating hamburger](www.cats.com/mcdonalds_pilferer.png)
        ![cat with bad markdown](www.cats.com/hacker_cat.jpg
        and a little bit
        of 
        regular
        text
        before the final cat
        ![cat holding trophy](www.cats.com/u_win.jpg)
        end!(lol)
        """
        matches = extract_markdown_images(text)
        expected = [
            ("cat licking its paw", "www.cats.com/paw_licker.jpg"),
            ("cat eating hamburger", "www.cats.com/mcdonalds_pilferer.png"),
            ("cat holding trophy", "www.cats.com/u_win.jpg"),
        ]
        self.assertListEqual(matches, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    pass
