import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    heading_pattern = r"^(#{1,6})\s+(.*)"
    quote_pattern = r"^>\s?(.*)"
    unordered_list_pattern = r"^[-+*]\s+(.*)"
    ordered_list_pattern = r"^(\d+)\.\s+(.*)"
    lines = block.splitlines()

    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if all(re.match(quote_pattern, line) for line in lines):
        return BlockType.QUOTE
    if re.match(heading_pattern, lines[0]):
        return BlockType.HEADING
    if all(re.match(unordered_list_pattern, line) for line in lines):
        return BlockType.ULIST

    orderd_list_match = []
    for i in range(len(lines)):
        line_match = re.match(ordered_list_pattern, lines[i])
        if line_match  and int(line_match.group(1)) == i + 1:
            orderd_list_match.append(True)
        else:
            orderd_list_match.append(False)

    if all(orderd_list_match):
        return BlockType.OLIST

    return BlockType.PARAGRAPH
