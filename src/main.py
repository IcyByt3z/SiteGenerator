from textnode import TextNode, TextType


def main():
    # 1. Instantiate the object and save it to a variable label
    node = TextNode(
        text="This is some anchor text",
        text_type=TextType.LINK,
        url="https://www.boot.dev"
    )

    # 2. Print it to the terminal to verify the __repr__ string formatting works!
    print(node)


if __name__ == "__main__":
    main()
