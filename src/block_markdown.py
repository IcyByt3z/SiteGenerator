from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class InvalidMarkdownError(Exception):
    """Raised when a markdown document is missing its main H1 title header."""


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in raw_blocks:
        block = block.strip()
        if block == "":
            continue
        cleaned_blocks.append(block)
    return cleaned_blocks


def block_to_block_type(block: str) -> BlockType:
    # 1. HEADING CHECK
    parts = block.split(" ", 1)
    if len(parts) > 1:
        prefix = parts[0]
        if 1 <= len(prefix) <= 6 and prefix == "#" * len(prefix):
            return BlockType.HEADING

    # 2. CODE BLOCK CHECK
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Split the block into individual lines to scan multi-line structural patterns
    lines = block.split("\n")

    # 3. QUOTE BLOCK CHECK
    is_quote = True
    for line in lines:
        if not line.strip().startswith(">"): # Added .strip() to bypass ghost spaces
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # 4. UNORDERED LIST CHECK
    is_unordered = True
    for line in lines:
        cleaned_line = line.strip()
        # Guard: If there is an accidental blank ghost line, skip it or check it
        if cleaned_line == "":
            continue
        if not cleaned_line.startswith(("- ", "* ")):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST

    # 5. ORDERED LIST CHECK
    is_ordered = True
    expected_number = 1
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue
        prefix = f"{expected_number}. "
        if not cleaned_line.startswith(prefix):
            is_ordered = False
            break
        expected_number += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    # 6. FALLBACK
    return BlockType.PARAGRAPH



def text_to_children(text: str) -> list:
    """Takes a string of text, runs it through the inline markdown filter,

    and translates the resulting TextNodes into renderable HTML LeafNodes.
    """
    text_nodes = text_to_textnodes(text)
    html_children = []
    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children


# ==========================================================
# 3. INDIVIDUAL STRUCTURAL BLOCK BUILDERS
# ==========================================================
def _create_heading_node(block: str) -> ParentNode:
    # Count the number of hashes to determine the heading level (h1 - h6)
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    # Strip the hashes and the leading space
    text_content = block[level + 1 :]
    return ParentNode(tag=f"h{level}", children=text_to_children(text_content))


def _create_code_node(block: str) -> ParentNode:
    # Strip the opening and closing backticks (and the mandatory newline)
    # Target: ```\ncode``` -> code
    text_content = block[4:-3]
    # Specialized requirement: No inline markdown parsing inside code tags!
    # We create a single raw text LeafNode container natively.
    code_leaf = LeafNode(tag="code", value=text_content)
    return ParentNode(tag="pre", children=[code_leaf])


def _create_quote_node(block: str) -> ParentNode:
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        # Strip the leading '>' symbol and any single leading space right after it
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        else:
            cleaned_lines.append(line[1:])
    # Combine the quote text blocks back together using standard spaces or newlines
    full_text = " ".join(cleaned_lines)
    return ParentNode(tag="blockquote", children=text_to_children(full_text))


def _create_unordered_list_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # FIX: Passing a tuple of prefixes to check both at the same time!
        if line.startswith(("- ", "* ")):
            item_text = line[2:]
        else:
            item_text = line

        list_items.append(ParentNode(tag="li", children=text_to_children(item_text)))

    return ParentNode(tag="ul", children=list_items)


def _create_ordered_list_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Ordered prefixes look like '1. ', '10. ', etc. Split at the first space!
        parts = line.split(" ", 1)
        item_text = parts[1] if len(parts) > 1 else ""
        list_items.append(ParentNode(tag="li", children=text_to_children(item_text)))
    return ParentNode(tag="ol", children=list_items)


def _create_paragraph_node(block: str) -> ParentNode:
    # Paragraphs take raw blocks as-is, replacing internal single line breaks with a space
    full_text = " ".join(block.split("\n"))
    return ParentNode(tag="p", children=text_to_children(full_text))


# ==========================================================
# 4. THE GRAND FINALE COMPILER ENGINE
# ==========================================================
def markdown_to_html_node(markdown: str) -> ParentNode:
    # Step 1: Slice the massive string into structural blocks
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    # Step 2: Loop over each block string and route it to its specific HTML builder
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            block_nodes.append(_create_heading_node(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(_create_code_node(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(_create_quote_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(_create_unordered_list_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(_create_ordered_list_node(block))
        else:
            block_nodes.append(_create_paragraph_node(block))

    # Step 3: Bundle all generated structural components under a single master div container
    return ParentNode(tag="div", children=block_nodes)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    raise InvalidMarkdownError(
        "Invalid Markdown: Document must contain at least one H1 heading (# )."
    )
