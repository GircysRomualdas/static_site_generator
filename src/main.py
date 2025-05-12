from copy_directory import transfer_content
from generate_content import generate_pages_recursive
import os

def main():
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.abspath(os.path.join(current_dir_path, ".."))

    static_path = os.path.join(project_root_path, "static")
    public_path = os.path.join(project_root_path, "public")
    transfer_content(static_path, public_path)

    from_path = os.path.join(project_root_path, "content")
    template_path = os.path.join(project_root_path, "template.html")
    destination_path = os.path.join(project_root_path, "public")
    generate_pages_recursive(from_path, template_path, destination_path)

if __name__ == "__main__":
    main()
