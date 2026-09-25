import unittest

from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("Hello *world*", TextType.TEXT)], "*", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("Hello ", TextType.TEXT), TextNode("world", TextType.BOLD)])

    def test_delimiter_no_match(self):
        nodes = split_nodes_delimiter([TextNode("Hello world", TextType.TEXT)], "*", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("Hello world", TextType.TEXT)])

    def test_delimiter_invalid_markdown(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("Hello *world", TextType.TEXT)], "*", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
