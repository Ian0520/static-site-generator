import sys

from src.helper import copy_static
from src.generate import generate_pages_recursive

STATIC = "static"
DEST = "docs"

CONTENT = "content"
TEMPLATE = "template.html"

def main():
    basepath = sys.argv[0] if sys.argv else "/"
    copy_static(STATIC, DEST)
    generate_pages_recursive(CONTENT, TEMPLATE, DEST, basepath)

main()