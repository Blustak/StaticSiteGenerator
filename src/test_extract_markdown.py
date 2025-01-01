import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


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
    def test_single_match(self):
        text = """
        a bit of text with a single link in it
        this is [my link](www.google.com)
        and this is the end of the string.
        """

        matches = extract_markdown_links(text)
        expected = [("my link", "www.google.com")]
        self.assertListEqual(matches, expected)

    def test_boot_dev_example(self):
        text = (
            "This is text with a link [to boot dev]"
            + "(https://www.boot.dev) and "
            + "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(matches, expected)

    def test_multi_match(self):
        text = """
        This is a test with multiple [links](wikipedia.com)
        there are many [links](wikipedia.com) in this, including
        some mistyped ones like [this][google.com]. However,
        my program should be able to identify 
        [which ones are right](good.com), and which ones are
        [bad(naughty.ru)
        for example, this is a bad [link] (because there's a space!)
        as is this one [here,
        because it is spread over multiple lines]
        """
        matches = extract_markdown_links(text)
        expected = [
            ("links", "wikipedia.com"),
            ("links", "wikipedia.com"),
            ("which ones are right", "good.com"),
        ]
        self.assertListEqual(matches, expected)


class TestExtractMarkdownBoth(unittest.TestCase):
    def test_both(self):
        text = """
        this test checks to see if the functions can distinguish
        between images and links in markdown.
        an image is like this ![cat](cats.co.uk)
        and a link is like this [dog](dogs.cz)
        did you get it right?
        """
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        expected_links = [("dog", "dogs.cz")]
        expected_images = [("cat", "cats.co.uk")]
        self.assertListEqual(links, expected_links)
        self.assertListEqual(images, expected_images)
