import os
import shutil

def transfer_content(source_path, destination_path):
    print("\nStart copying content\n")
    if not os.path.exists(source_path):
        raise ValueError("not valid source path")

    clear_directory(destination_path)
    copy_content(get_file_paths(source_path), destination_path)
    print("\nEnd copying content\n")

def get_file_paths(path):
    files = []

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            files.append((filename, file_path, None))
        else:
            files.append((filename, file_path, get_file_paths(file_path)))

    return files

def copy_content(source_paths, destination_path):
    for source_path in source_paths:
        source_filename = source_path[0]
        source_file_path = source_path[1]
        source_sub_dir_paths = source_path[2]
        destination_file_path = os.path.join(destination_path, source_filename)

        if source_sub_dir_paths is None:
            shutil.copy(source_file_path, destination_file_path)
            print(f"\tCopy file from {source_file_path} to {destination_file_path}")
        else:
            os.mkdir(destination_file_path)
            print(f"\tCreate {destination_file_path} directory")
            copy_content(source_sub_dir_paths, destination_file_path)

def clear_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"\tDelete old {path} directory and is content")

    os.mkdir(path)
    print(f"\tCreate empty {path} directory")
