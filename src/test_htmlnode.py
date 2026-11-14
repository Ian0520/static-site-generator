import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_children(self):
        child = HTMLNode("span", "child text")
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children, [child])

    def test_to_html_raises(self): 
        node = HTMLNode("p", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_format(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_repr(self):
        node = HTMLNode("p", "test", None, {"class": "primary"})
        expected = "HTMLNode(p, test, children: None, {'class': 'primary'})"
        self.assertEqual(repr(node), expected)
    