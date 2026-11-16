from src.helper import copy_static
from src.generate import generate_page

STATIC = "static"
PUBLIC = "public"

CONTENT = "content/index.md"
DEST = "public/index.html"
TEMPLATE = "template.html"

def main():
    copy_static(STATIC, PUBLIC)
    generate_page(CONTENT, TEMPLATE, DEST)

main()