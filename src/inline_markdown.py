import re

from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        # Step 1: Skip if it's already an active stylized formatting block
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        images = extract_markdown_images(current_text)

        # Step 2: If there are no images in this block, pass it through untouched
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        # Step 3: Loop through every discovered image pattern inside the sentence
        for image_alt, image_url in images:
            # Construct the exact markdown search token anchor target
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown: image split error")

            # If there is text before the image syntax, log it as raw text
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Append the beautifully extracted Image Node package
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            # Slide our text cursor forward to evaluate the remaining trailing text slice
            current_text = sections[1]

        # Step 4: After processing all images, if any trailing tail text remains, append it!
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        links = extract_markdown_links(current_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link_text, link_url in links:
            sections = current_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown: link split error")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

    # 1. ADD THIS IMPORT AT THE VERY TOP OF THE FILE:

    # ... (keep your existing extractors and splitters exactly how they are) ...

    # 2. ADD THIS MASTER FUNCTION AT THE ABSOLUTE BOTTOM OF THE FILE:
def text_to_textnodes(text: str) -> list[TextNode]:
    # Start with a single raw plain text node inside a list
    nodes = [TextNode(text, TextType.TEXT)]

    # Stage 1: Filter out bold markdown (**text**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Stage 2: Filter out italic markdown (*text*)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Stage 3: Filter out inline code blocks (`text`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Stage 4: Filter out markdown images (![alt](url))
    nodes = split_nodes_image(nodes)

    # Stage 5: Filter out markdown links ([anchor](url))
    nodes = split_nodes_link(nodes)

    return nodes
