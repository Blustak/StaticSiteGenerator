from textnode import TextNode, TextType
from htmlnode import LeafNode
from split_nodes import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
)


def text_to_text_node(text):
    nodes = [TextNode(text, TextType.TEXT)]
    images = split_nodes_image(nodes)
    links = split_nodes_link(images)
    bold = split_nodes_delimiter(links, "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "*", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    return code


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise Exception(f"TextType not recognised: {text_node.text_type}")
