from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    stripped = []
    blocks = markdown.split("\n\n")

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            stripped.append(stripped_block) 

    return stripped


def block_to_block_type(md):
    # lines
    lines = md.split("\n")
    is_quote = True
    is_unordered = True
    is_ordered = True

    if re.search(r"^(#{1,6}\s{1})", md):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    for i in range(len(lines)):
        if lines[i][0] != ">":
            is_quote = False
        
        if re.search(r"^-{1}\s{1}", lines[i]) is None:
            is_unordered = False

        pattern = f"^{i + 1}\.\s"
        if re.search(pattern, lines[i]) is None:
            is_ordered = False

    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH