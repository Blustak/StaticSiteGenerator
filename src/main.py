from textnode import TextNode, TextType


def main():
    node = TextNode(
        "hello world",
        TextType.ITALIC,
    )
    print(node)


if __name__ == "__main__":
    main()
