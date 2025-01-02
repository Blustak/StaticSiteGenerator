"""
Functions required for extracting metadata from markdown.
"""

import re


def extract_markdown_images(text):
    """
    returns a list of tuples, where each tuple contains the alt text
    and the URL.

    Example: "This text contains ![cat](www.cat.com/cat.jpg) a cool cat!"
    returns: [("cat", "www.cat.com/cat.jpg")]
    """

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    """
    returns a list of tuples, where each tuple contains the anchor text
    and the URL.

    Example: "This text contains [cat](www.cat.com/cat.jpg) a cool cat!"
    returns: [("cat", "www.cat.com/cat.jpg")]
    """

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
