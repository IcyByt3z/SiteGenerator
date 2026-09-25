from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        # Rule 1: We ONLY parse raw plain text nodes. Other nodes (like images or existing bold nodes) are skipped!
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        # If the delimiter isn't even in the text, pass it through untouched
        if delimiter not in text:
            new_nodes.append(old_node)
            continue

        # Slice the sentence apart at each delimiter instance
        split_text = text.split(delimiter)

        # CRITICAL SAFETY GATE: If a string splits into an EVEN number of pieces,
        # it means a delimiter symbol was never closed! (e.g., ["Hello ", "code"])
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown: sections with delimiter '{delimiter}' were never closed.")

        # Alternating parsing track
        for i, split in enumerate(split_text):
            # ACCUMULATION GUARD: Skip empty strings so we don't pollute our data structures
            if split == "":
                continue

            # If the index is odd, it's inside the delimiters! Tag it with the target style.
            # If the index is even, it's normal surrounding text.
            if i % 2 == 1:
                new_nodes.append(TextNode(split, text_type))
            else:
                new_nodes.append(TextNode(split, TextType.TEXT))

    return new_nodes
