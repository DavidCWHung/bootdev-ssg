import os
import shutil

from textnode import TextNode, TextType
from md_to_html_node import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
generate_page_from_path = "./content"
generate_page_template_path = "./template.html"
generate_page_to_path = "./public"


def delete_contents(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist")
        return

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path):
            os.remove(path)
            print(f"Removing file {path}")
        else:
            shutil.rmtree(path)
            print(f"Removing directory and files inside {path}")


def copy_contents(src, dst):
    if not os.path.exists(src):
        print(f"Directory {src} does not exist")
        return
    if not os.path.exists(dst):
        print(f"Directory {dst} does not exist")
        return

    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)

        if os.path.isfile(src_path):
            destination = shutil.copy(src_path, dst_path)
            print(f"Copying {src_path} to {destination}")
        else:
            os.mkdir(dst_path)
            print(f"Creating directory {dst_path}")
            destination = copy_contents(src_path, dst_path)


def main():
    delete_contents(dir_path_public)
    copy_contents(dir_path_static, dir_path_public)
    generate_pages_recursive(generate_page_from_path,
                  generate_page_template_path, generate_page_to_path)


main()
