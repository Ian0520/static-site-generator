

import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts)%2 == 0:
            raise ValueError("invalid markdown syntax")
        for i in range(len(parts)):
            if not parts[i]:
                continue
            if i % 2 == 0:
                result.append(TextNode(parts[i], TextType.TEXT))
            else:
                result.append(TextNode(parts[i], text_type))
    return result

def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    