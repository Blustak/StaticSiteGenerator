from textnode import TextType, TextNode


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
