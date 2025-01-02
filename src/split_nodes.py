from textnode import TextType, TextNode
from extract_markdown import extract_markdown_links, extract_markdown_images


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter,
    text_type: TextType,
):
    node_list = []
    for node in old_nodes:
        type_a = node.text_type
        type_b = text_type
        if node.text.startswith(delimiter):
            current_type = type_b
        else:
            current_type = type_a
        split_string = node.text.split(delimiter)
        for s in split_string:
            if len(s) > 0:
                node_list.append(TextNode(s, current_type))
                current_type = type_b if current_type is type_a else type_a
    return node_list


def split_nodes_image(old_nodes: list[TextNode]):
    nodes = []
    for node in old_nodes:
        original_type = node.text_type
        images = extract_markdown_images(node.text)
        images = list(reversed(images))

        if len(images) <= 0:
            nodes.append(node)
        else:
            text_to_process = node.text
            while len(text_to_process) > 0:
                # there's no more images to split by.
                # append the rest of the text and return
                if len(images) <= 0:
                    nodes.append(TextNode(text_to_process, original_type))
                    break

                (alt, url) = images.pop()
                delim = f"![{alt}]({url})"
                splits = text_to_process.split(delim, 1)
                if len(splits) == 1:
                    nodes.append(TextNode(splits[0], original_type))
                else:
                    (text, text_to_process) = (splits[0], splits[1])
                    if len(text) > 0:
                        nodes.append(TextNode(text, original_type))
                    nodes.append(TextNode(alt, TextType.IMAGE, url))

    return nodes


def split_nodes_link(old_nodes: list[TextNode]):
    nodes = []
    for node in old_nodes:
        original_type = node.text_type
        links = extract_markdown_links(node.text)
        links = list(reversed(links))

        if len(links) <= 0:
            nodes.append(node)
        else:
            text_to_process = node.text
            while len(text_to_process) > 0:
                # there's no more images to split by.
                # append the rest of the text and return
                if len(links) <= 0:
                    nodes.append(TextNode(text_to_process, original_type))
                    break

                (alt, url) = links.pop()
                delim = f"[{alt}]({url})"
                splits = text_to_process.split(delim, 1)
                if len(splits) == 1:
                    nodes.append(TextNode(splits[0], original_type))
                else:
                    (text, text_to_process) = (splits[0], splits[1])
                    if len(text) > 0:
                        nodes.append(TextNode(text, original_type))
                    nodes.append(TextNode(alt, TextType.LINK, url))

    return nodes
