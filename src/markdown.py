from src.block import BlockType, block_to_block_type, markdown_to_blocks
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.inline import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    tag = "div"
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)
    return ParentNode(tag, children)

def block_to_html_node(block: str, block_type) -> ParentNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)

def paragraph_to_html_node(block: str) -> ParentNode:
    tag = "p"
    text = " ".join(block.split('\n'))
    children = text_to_children(text)
    return ParentNode(tag, children)

def heading_to_html_node(block: str) -> ParentNode:
    tag = f"h{len(block.split()[0])}"
    text = block.split(maxsplit=1)[1]
    children = text_to_children(text)
    return ParentNode(tag, children)

def code_to_html_node(block: str) -> ParentNode:
    tag = "code"
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    children = [text_node_to_html_node(text_node)]
    code_node = ParentNode(tag, children)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block: str) -> ParentNode:
    tag = "blockquote"
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode(tag, children)

def unordered_list_to_html_node(block: str) -> ParentNode:
    tag = "ul"
    lines = block.split('\n')
    children = unordered_list_lines_to_html_nodes(lines)
    return ParentNode(tag, children)

def unordered_list_lines_to_html_nodes(lines: list[str]) -> list[ParentNode]:
    result = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        result.append(ParentNode("li", children))
    return result

def ordered_list_to_html_node(block: str) -> ParentNode:
    tag = "ol"
    lines = block.split('\n')
    children = ordered_list_lines_to_html_nodes(lines)
    return ParentNode(tag, children)

def ordered_list_lines_to_html_nodes(lines: list[str]) -> list[ParentNode]:
    result = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        result.append(ParentNode("li", children))
    return result
    

def text_to_children(text) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children = [
        text_node_to_html_node(text_node) for text_node in text_nodes
    ]
    return children