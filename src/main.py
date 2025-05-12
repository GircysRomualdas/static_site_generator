from copy_directory import transfer_content
from generate_content import generate_pages_recursive
import os
import sys

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"

    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.abspath(os.path.join(current_dir_path, ".."))

    static_path = os.path.join(project_root_path, "static")
    public_path = os.path.join(project_root_path, "docs")
    transfer_content(static_path, public_path)

    from_dir_path = os.path.join(project_root_path, "content")
    template_path = os.path.join(project_root_path, "template.html")
    destination_dir_path = os.path.join(project_root_path, "docs")
    print("\nStart generating pages\n")
    generate_pages_recursive(from_dir_path, template_path, destination_dir_path, basepath)
    print("\nEnd generating pages\n")

if __name__ == "__main__":
    main()
