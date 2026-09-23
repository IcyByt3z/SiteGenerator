from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
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
        return f"TextNode({self.text_type}, {self.text}, {self.url})"

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
