import sys

from src.helper import copy_static
from src.generate import generate_pages_recursive

STATIC = "static"
DEST = "docs"

CONTENT = "content"
TEMPLATE = "template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)
    copy_static(STATIC, DEST)
    generate_pages_recursive(CONTENT, TEMPLATE, DEST, basepath)

main()