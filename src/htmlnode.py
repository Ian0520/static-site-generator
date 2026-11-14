class HTMLNode:
    def __init__(
        self, 
        tag: str | None = None, 
        value: str | None = None, 
        children: list["HTMLNode"] | None = None, 
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props: return ""
        result = ""
        for attribute in self.props:
            result += f" {attribute}=\"{self.props[attribute]}\""
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        

class LeafNode(HTMLNode):
    def __init__(
        self, 
        tag: str | None, 
        value: str, 
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            tag=tag, 
            value=value, 
            props=props,
        )

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("leaf node has no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
            