import unittest

from src.block import BlockType, block_to_block_type, markdown_to_blocks

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_newline(self):
        md = """
This paragraph has a bunch of newlines





- and a list
- with items     
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph has a bunch of newlines",
                "- and a list\n- with items",
            ]
        )
    def test_strip_leading_space(self):
        md = """
   This paragraph has leading spaces.

  This paragraph also has leading spaces.

      More leading spaces.
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph has leading spaces.",
                "This paragraph also has leading spaces.",
                "More leading spaces.",
            ]
        )

    def test_block_to_block_type_heading(self):
        block = "###### This is a heading. "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_empty_not_heading(self):
        block = "##"
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```\nthis is a coding block```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote"
        block2 = ">This is also a quote"
        block_type = block_to_block_type(block)
        block_type2 = block_to_block_type(block2)
        self.assertEqual(block_type, BlockType.QUOTE)
        self.assertEqual(block_type2, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- item1
- item2
- item3"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. item1
2. item2
3. item3"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong_number(self):
        block = """1. item1
6. item2
3. item3"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)