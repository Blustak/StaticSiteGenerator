class HTMLNode:

    def __init__(
        self,
        tag=None,
        value=None,
        children=None,
        props=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(
            map(
                lambda x: f' {x[0]}="{x[1]}"',
                self.props.items(),
            )
        )

    def __repr__(self):
        output = "HTMLNode:("
        if self.tag is not None:
            output += f"tag:{self.tag}, "
        else:
            output += "tag:None, "
        if self.value is not None:
            output += f"value:{self.value}, "
        else:
            output += "value:None, "
        if self.children is not None:
            output += "children: ["
            output += "\n".join(self.children)
            output += "],\n"
        else:
            output += "children:None, "
        if self.props is not None:
            output += f"props: {self.props}"
        else:
            output += "props:None, "
        return output + "]"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    # Tag and Children are not optional.
    # Parent nodes do not have values
    # props are optional
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Error: tag of {self} cannot be NoneType")
        if self.children is None:
            raise ValueError(
                f"Error: children property of {self} cannot be NoneType",
            )
        else:
            return (
                f"<{self.tag}{self.props_to_html()}>"
                + "".join(map(lambda x: x.to_html(), self.children))
                + f"</{self.tag}>"
            )
