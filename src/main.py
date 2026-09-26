import os
import shutil
import sys

from block_markdown import extract_title, markdown_to_html_node


def copy_directory_recursive(source_dir: str, dest_dir: str) -> None:
    if not os.path.exists(source_dir):
        return
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    items = os.listdir(source_dir)
    for item in items:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(src_path):
            copy_directory_recursive(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(
        f"📄 Generating page from '{from_path}' to '{dest_path}' using template '{template_path}' with basepath '{basepath}'..."
    )

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node_tree = markdown_to_html_node(markdown_content)
    html_string = html_node_tree.to_html()

    page_title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_string)

    # CRITICAL PRODUCTION SWAP: Prepend the custom GitHub basepath to absolute links & images!
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)

        if os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir, basepath)

        elif os.path.isfile(src_path) and item.endswith(".md"):
            html_filename = item.replace(".md", ".html")
            dest_file_path = os.path.join(dest_dir_path, html_filename)

            generate_page(src_path, template_path, dest_file_path, basepath)


def main():
    # 1. READ THE BASEPATH FROM CLI ARGUMENTS: Default to "/" if none provided
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    source_folder = "static"
    # 2. UPDATE TARGET DIRECTORY TO DOCS FOR GITHUB PAGES!
    destination_folder = "docs"

    print(f"🔧 Target deployment basepath configured to: '{basepath}'")
    print("🧹 Cleaning up old deployment builds...")
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    print("🚀 Initiating recursive static assets transfer...")
    copy_directory_recursive(source_folder, destination_folder)

    print("🎨 Launching recursive multi-page compilation sequence...")
    generate_pages_recursive("content", "template.html", destination_folder, basepath)
    print("🎉 All pages successfully generated and published to /docs!")


if __name__ == "__main__":
    main()
