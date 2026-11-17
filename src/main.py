import sys

from src.helper import copy_static
from src.generate import generate_pages_recursive

STATIC = "static"
DOCS = "docs"

CONTENT = "content"
DEST = "public"
TEMPLATE = "template.html"

def main():
    basepath = sys.argv[0] if sys.argv else "/"
    copy_static(STATIC, DOCS)
    generate_pages_recursive(CONTENT, TEMPLATE, DEST, basepath)

main()