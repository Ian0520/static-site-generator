

import os

from src.markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
        
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(new_page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for target in os.listdir(dir_path_content):
        old = os.path.join(dir_path_content, target)
        html_file = target.rstrip(".md") + ".html"
        new_file = os.path.join(dest_dir_path, html_file)
        if os.path.isfile(old):
            generate_page(old, template_path, new_file)
        else:
            new_folder = os.path.join(dest_dir_path, target)
            generate_pages_recursive(old, template_path, new_folder)