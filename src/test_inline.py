

import unittest

from src.inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](www.google.com) and another [link2](www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "www.youtube.com"),
            ],
            new_nodes
        )

    def test_split_images_none(self):
        node = TextNode(
            "This is a **text without [link] or image!",
            TextType.TEXT,
        )
        self.assertEqual([node], split_nodes_image([node]))

    def test_split_links_none(self):
        node = TextNode(
            "This is a **text without [link] or image!",
            TextType.TEXT,
        )
        self.assertEqual([node], split_nodes_link([node]))

    def test_split_only_image(self):
        node = TextNode(
            "![only image](www.imgur.com/image.png)",
            TextType.TEXT
        )
        expected = [
            TextNode("only image", TextType.IMAGE, "www.imgur.com/image.png")
        ]
        self.assertEqual(expected, split_nodes_image([node]))

    def test_split_only_link(self):
        node = TextNode(
            "[only link](www.google.com)",
            TextType.TEXT,
        )
        expected = [
            TextNode("only link", TextType.LINK, "www.google.com")
        ]
        self.assertEqual(expected, split_nodes_link([node]))