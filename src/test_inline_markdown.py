import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://imgur.com) and another ![second image](https://imgur.com)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [("image", "https://imgur.com"), ("second image", "https://imgur.com")],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://boot.dev) and [to youtube](https://youtube.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("to boot dev", "https://boot.dev"),
                ("to youtube", "https://youtube.com"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://imgur.com)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgur.com"),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://boot.dev)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_nodes_multi_image(self):
        node = TextNode(
            "This is text with an ![image](https://imgur.com) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # FIX: The assertion properly maps the remaining text tail segment!
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgur.com"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obama pfp](https://imgur.com) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obama pfp", TextType.IMAGE, "https://imgur.com"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
