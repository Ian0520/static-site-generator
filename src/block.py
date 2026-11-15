from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    for block in markdown.split('\n\n'):
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)
    return result

