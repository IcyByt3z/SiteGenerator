from enum import Enum

# FIX 1: Only import LeafNode. Do NOT try to import a function you are writing here!
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"  # Boot.dev uses 'TEXT' or 'NORMAL' (This matches your current layout)
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


# FIX 2: Completely left-aligned against the margin (not indented inside the class!)
# FIX 3: Named exactly text_node_to_html_node to match your pipeline expectations
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url},  # type: ignore
        )

    elif text_node.text_type == TextType.IMAGE:
        # Images require an empty value string in clean HTML compilation structures!
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text},  # type: ignore
        )

    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
