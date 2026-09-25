

class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        html_attributes = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(html_attributes)

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    # Your required constructor signature (Do not change this!)
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        # CRITICAL REASONING FIX: This intercepts 'None' values and throws the error your test expects!
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode must have children")

        # Standard recursive compilation loops
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
