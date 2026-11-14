

import unittest

from src.inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestInline(unittest.TestCase):
    def test_delimiter_at_start(self):
        node = TextNode("**this** is a bold text", TextType.TEXT)
        expected = [
            TextNode("this", TextType.BOLD),
            TextNode(" is a bold text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_delimeter_at_middle(self):
        node = TextNode("this **is a bold** text", TextType.TEXT)
        expected = [
            TextNode("this ", TextType.TEXT),
            TextNode("is a bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected) 

    def test_delimeter_at_end(self):
        node = TextNode("this is a bold **text**", TextType.TEXT)
        expected = [
            TextNode("this is a bold ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected) 

    def test_multple_same_delimeters(self):
        node = TextNode("**this** has **multiple** bold", TextType.TEXT)
        expected = [
            TextNode("this", TextType.BOLD),
            TextNode(" has ", TextType.TEXT),
            TextNode("multiple", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_unmatched_delimeter(self):
        node = TextNode("This code is `unmatched", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_kinds_of_nodes(self):
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("this contains _italic_ text", TextType.TEXT),
            TextNode("regular text", TextType.TEXT),
        ]
        expected = [
            TextNode("bold text", TextType.BOLD),
            TextNode("this contains ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("regular text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [link](www.google.com)"
        )
        self.assertEqual([("link", "www.google.com")], matches)

    def test_images_not_extracted_as_link(self):
        matches = extract_markdown_links(
            "This is a text with ![not a link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

    def test_extract_images_none(self):
        matches = extract_markdown_images(
            "This is a **regular** text"
        )
        self.assertEqual([], matches)

    def test_extract_links_none(self):
        matches = extract_markdown_links(
            "This is a `regular` text"
        )
        self.assertEqual([], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "this has multiple images! ![image1](imgur.com/example.png) ![image2](imgur.com/example2.png)"
        )
        self.assertEqual(
            [
                ("image1", "imgur.com/example.png"),
                ("image2", "imgur.com/example2.png"),
            ],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "this has multiple links! [link1](www.google.com) [link2](www.youtube.com)"
        )
        self.assertEqual(
            [
                ("link1", "www.google.com"),
                ("link2", "www.youtube.com"),
            ],
            matches
        )
