import re
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    heading_pattern = r"^# (.+)$"
    match = re.search(heading_pattern, markdown, re.MULTILINE)

    if not match:
        raise Exception("no header")

    return match.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = None
    template_contents = None

    with open(from_path, "r") as data:
        markdown_contents = data.read()
    with open(template_path, "r") as data:
        template_contents = data.read()

    md_html = markdown_to_html_node(markdown_contents).to_html()
    md_title = extract_title(markdown_contents)
    new_html = template_contents.replace("{{ Content }}", md_html).replace("{{ Title }}", md_title)

    with open(dest_path, "w") as data:
        data.write(new_html)
