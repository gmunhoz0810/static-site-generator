import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHMTLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_constructor_sets_fields(self):
        node = HTMLNode(tag='p', value='Hello', children=[], props={'id': 'paragraph'})
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'id': 'paragraph'})    

    def test_repr_method(self):
        node = HTMLNode(tag='div', value='Test', children=[], props={'class': 'container'})
        self.assertEqual(repr(node), "HTMLNode(div, Test, [], {'class': 'container'})")

    def test_leaf_node_to_html_with_tag_and_props(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_node_to_html_with_tag_no_props(self):
        node = LeafNode("This is a paragraph.", "p")
        self.assertEqual(node.to_html(), '<p>This is a paragraph.</p>')
    
    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode("Just some text.")
        self.assertEqual(node.to_html(), 'Just some text.')
    
    def test_leaf_node_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode(None).to_html()

    
class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        node = ParentNode(
            [
                LeafNode("Hello world", "p"),
            ],
            "div"
        )
        self.assertEqual(node.to_html(), '<div><p>Hello world</p></div>')

    def test_parent_node_nested(self):
        node = ParentNode(
            [
                ParentNode(
                    [
                        LeafNode("Bold text", "b"),
                        LeafNode("Normal text"),
                        LeafNode("italic text", "i"),
                        LeafNode("Normal text"),
                    ],
                    "p"
                ),
            ],
            "div"
        )
        expected_html = '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_props(self):
        node = ParentNode(
            [
                LeafNode("Some link", "a", {"href": "https://www.google.com"}),
            ],
            "div",
            {"class": "container"}
        )
        self.assertEqual(node.to_html(), '<div class="container"><a href="https://www.google.com">Some link</a></div>')

    def test_parent_node_no_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode([LeafNode("Hello world")], None).to_html()

    def test_parent_node_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode([], "div").to_html()

    def test_mixed_parent_and_leaf_nodes(self):
        node = ParentNode(
            [
                LeafNode("This is a title", "h1"),
                ParentNode(
                    [
                        LeafNode("This is a paragraph", "p"),
                        LeafNode("Another paragraph", "p"),
                    ],
                    "div"
                ),
                LeafNode("This is a footer", "footer"),
            ],
            "section"
        )
        expected_html = (
            '<section>'
            '<h1>This is a title</h1>'
            '<div><p>This is a paragraph</p><p>Another paragraph</p></div>'
            '<footer>This is a footer</footer>'
            '</section>'
        )
        self.assertEqual(node.to_html(), expected_html)

                         
if __name__ == '__main__':
    unittest.main()
