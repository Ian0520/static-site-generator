from enum import Enum

from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: str|None = None,
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type.value == other.text_type.value
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text})
        case _:
            raise ValueError("text type does not exist")
        
    