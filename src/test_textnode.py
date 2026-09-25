import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_init(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)  # Clean python check for None values

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        # FIX: Swapped the layout so 'This is a text node' comes before 'bold'!
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")


if __name__ == "__main__":
    unittest.main()
