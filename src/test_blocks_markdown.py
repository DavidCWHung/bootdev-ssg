import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_heading1(self):
        md = "# This is Heading 1"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, type)

    def test_block_to_block_type_heading6(self):
        md = "###### This is Heading 6"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, type)

    def test_block_to_block_type_paragraph(self):
        md = "####### This is a paragraph"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_block_to_block_type_code(self):
        md = "```\nThis is a code block\n```"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, type)

    def test_block_to_block_type_code_with_space(self):
        md = "```\nThis is a code block !!!!    \n```"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, type)

    def test_block_to_block_type_code_with_quote(self):
        md = ">this is a quote"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, type)

    def test_block_to_block_type_code_with_unordered(self):
        md = "- unordered 1\n- unordered 2\n- unordered3"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, type)

    def test_block_to_block_type_code_with_ordered(self):
        md = "1. unordered 1\n2. unordered 2\n3. unordered3"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, type)

    def test_block_to_block_type_code_with_ordered_start_from_2(self):
        md = "2. unordered 1\n2. unordered 2\n3. unordered3"
        type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
