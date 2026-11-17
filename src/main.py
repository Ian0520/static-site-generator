from src.helper import copy_static
from src.generate import generate_pages_recursive

STATIC = "static"
PUBLIC = "public"

CONTENT = "content"
DEST = "public"
TEMPLATE = "template.html"

def main():
    copy_static(STATIC, PUBLIC)
    generate_pages_recursive(CONTENT, TEMPLATE, DEST)

main()