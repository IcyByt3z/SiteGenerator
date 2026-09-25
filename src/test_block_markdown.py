import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** words and an *italic* word.

* This is the first list item.
* This is a second list item."""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** words and an *italic* word.",
                "* This is the first list item.\n* This is a second list item.",
            ],
        )

    def test_markdown_to_blocks_excess_newlines(self):
        # Additional coverage: Verifies that multiple random whitespace line drops get collapsed cleanly
        md = """# Heading


Paragraph with space


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph with space"])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Invalid headings fall back to paragraph
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpaceHeading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        code_block = "```\ndef my_func():\n    return 42\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        # Broken backtick structures fall back to paragraph
        self.assertEqual(
            block_to_block_type("```def my_func()```"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        quote_block = "> This is a quote line.\n> This is the second line."
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        # One line missing the > symbol falls back to paragraph
        bad_quote = "> Line 1\nLine 2 missing wrapper"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        ul_block = "- Item A\n- Item B\n- Item C"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)
        # Missing space falls back to paragraph
        bad_ul = "- Item A\n-Item B without space"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        ol_block = "1. First thing\n2. Second thing\n3. Third thing"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)
        # Broken sequence numbering falls back to paragraph
        bad_ol_sequence = "1. Item 1\n3. Item 3 jumped out of order"
        self.assertEqual(block_to_block_type(bad_ol_sequence), BlockType.PARAGRAPH)
        # Starting at 0 falls back to paragraph
        bad_ol_start = "0. Wrong start\n1. Item 1"
        self.assertEqual(block_to_block_type(bad_ol_start), BlockType.PARAGRAPH)

    def test_markdown_to_html_node(self):
            # 1. Your raw markdown document input string
            md = """# Main Header

This is a paragraph with **bold** text."""

            # 2. Fire your engine to generate the nested HTMLNode tree
            html_node = markdown_to_html_node(md)

            # 3. Define EXACTLY what string format the browser should receive
            expected_html = (
                "<div>"
                "<h1>Main Header</h1>"
                "<p>This is a paragraph with <strong>bold</strong> text.</p>"
                "</div>"
            )

            # 4. CRITICAL CHECKPOINT: Ensure the generated HTML matches our expectation!
            self.assertEqual(html_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
