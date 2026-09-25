import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # ==========================================
    # BASE HTMLNODE TESTS
    # ==========================================
    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_values_initialization(self):
        node = HTMLNode(tag="h1", value="Welcome")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Welcome")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode(tag="span", value="text")
        self.assertIn("span", repr(node))
        self.assertIn("text", repr(node))

    # ==========================================
    # LEAF NODE TESTS
    # ==========================================
    def test_leaf_node_p(self):
        node = LeafNode(tag="p", value="text")
        self.assertEqual(node.to_html(), "<p>text</p>")

    def test_leaf_node_span(self):
        node = LeafNode(tag="span", value="text")
        self.assertEqual(node.to_html(), "<span>text</span>")

    def test_leaf_node_no_tag(self):
        node = LeafNode(value="text")
        self.assertEqual(node.to_html(), "text")

    def test_leaf_node_with_props(self):
        node = LeafNode(
            tag="a", value="Click here", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click here</a>'
        )

    # ==========================================
    # PARENT NODE TESTS (CALIBRATED & SAFE)
    # ==========================================
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node])
        # FIX: Converted to clean unittest syntax for precision output
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", children=[grandchild_node])
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", children=[child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", children=[])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        parent_node = ParentNode("div", children=[], props={"class": "test"})
        self.assertEqual(parent_node.to_html(), '<div class="test"></div>')

    def test_to_html_deeply_nested(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node], props={"class": "test"})
        grandparent_node = ParentNode(
            "div", children=[parent_node], props={"class": "test"}
        )
        grandgrandparent_node = ParentNode(
            "div", children=[grandparent_node], props={"class": "test"}
        )

        expected_output = '<div class="test"><div class="test"><div class="test"><span>child</span></div></div></div>'
        self.assertEqual(grandgrandparent_node.to_html(), expected_output)

    # ==========================================
    # CRITICAL ADDITION: CRASH / ERROR VALIDATIONS
    # ==========================================
    def test_parent_node_missing_tag(self):
        # We add '# type: ignore' at the end of the line to tell Zed:
        # "Shh, I know I'm passing None here on purpose to test the crash rule!"
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[LeafNode("b", "text")])  # type: ignore
            node.to_html()

    def test_parent_node_missing_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="div", children=None)  # type: ignore
            node.to_html()




if __name__ == "__main__":
    unittest.main()
