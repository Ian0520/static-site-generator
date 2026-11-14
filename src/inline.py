

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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        images_extracted = extract_markdown_images(old_node.text)
        text_left = old_node.text
        for image in images_extracted:
            alt = image[0]
            url = image[1]
            parts = text_left.split(f"![{alt}]({url})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            text_left = parts[1]
        if text_left:
            result.append(TextNode(text_left, TextType.TEXT))
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        links_extracted = extract_markdown_links(old_node.text)
        text_left = old_node.text
        for link in links_extracted:
            alt = link[0]
            url = link[1]
            parts = text_left.split(f"[{alt}]({url})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.LINK, url))
            text_left = parts[1]
        if text_left:
            result.append(TextNode(text_left, TextType.TEXT))
    return result

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes