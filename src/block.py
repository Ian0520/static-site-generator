from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    for block in markdown.split('\n\n'):
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    headings_start = ['#' * i for i in range(1,7)]
    if block.split()[0] in headings_start and len(block.split()) > 1:
        return BlockType.HEADING
        
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
        
    if block.startswith('>') and len(block) > 1:
        return BlockType.QUOTE
        
    for line in block.split('\n'):
        if not line.startswith('- '):
            break
    else:
        return BlockType.UNORDERED_LIST

    num = 1
    for line in block.split('\n'):
        if not line.startswith(f'{num}. '):
            break
        num += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH