import re
import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    heading_pattern = r"^# (.+)$"
    match = re.search(heading_pattern, markdown, re.MULTILINE)

    if not match:
        raise Exception("no header")

    return match.group(1)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"\tGenerating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = None
    template_contents = None

    with open(from_path, "r") as data:
        markdown_contents = data.read()
    with open(template_path, "r") as data:
        template_contents = data.read()

    md_html = markdown_to_html_node(markdown_contents).to_html()
    md_title = extract_title(markdown_contents)
    new_html = template_contents.replace("{{ Content }}", md_html).replace("{{ Title }}", md_title)

    if basepath.endswith('/') and basepath != '/':
        basepath = basepath[:-1]

    new_html = new_html.replace('href="/', f'href="{basepath}/')
    new_html = new_html.replace('src="/', f'src="{basepath}/')

    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w") as data:
        data.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)

    for filename in os.listdir(dir_path_content):
        src_file_path = os.path.join(dir_path_content, filename)

        if os.path.isfile(src_file_path):
            name, ext = os.path.splitext(filename)

            if ext == ".md":
                dest_file_path = os.path.join(dest_dir_path, f"{name}.html")
                generate_page(src_file_path, template_path, dest_file_path, basepath)
        else:
            dest_subdir_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(src_file_path, template_path, dest_subdir_path, basepath)
