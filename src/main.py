import os
import shutil

# Import your master block compiling systems from yesterday
from block_markdown import extract_title, markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    """Recursively crawls the entire content folder, automatically compiling every

    markdown (.md) file it discovers into a matching HTML file structure.
    """
    # 1. Grab a clean list of all items inside the current content folder
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)

        # Case A: If it's a subfolder, use recursion to dive deeper into the rabbit hole!
        if os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir)

        # Case B: If it's a file AND it ends in '.md', compile it!
        elif os.path.isfile(src_path) and item.endswith(".md"):
            # Calculate the destination path name (swap .md out for a clean .html wrapper)
            html_filename = item.replace(".md", ".html")
            dest_file_path = os.path.join(dest_dir_path, html_filename)

            # Fire off our single page generator tool to write it to disk!
            generate_page(src_path, template_path, dest_file_path)


def copy_directory_recursive(source_dir: str, dest_dir: str) -> None:
    """Recursively walks through a source directory and copies every single

    file and nested subfolder into a destination path.
    """
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


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Reads a markdown article file, parses its layout structures, binds it

    inside an HTML template skin, and dumps the file to your hard drive.
    """
    print(
        f"📄 Generating page from '{from_path}' to '{dest_path}' using template '{template_path}'..."
    )

    # 1. Ingest the source files off the local disk drive
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template skin layout file not found: {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 2. Execute our multi-stage compiler translations
    html_node_tree = markdown_to_html_node(markdown_content)
    html_string = html_node_tree.to_html()

    page_title = extract_title(markdown_content)

    # 3. Splice our string values inside our template placeholder hooks
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_string)

    # 4. Save the finished webpage out to our target directory path
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # FIXED: The bad read line is gone! We now safely write the html straight to disk.
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def main():
    source_folder = "static"
    destination_folder = "public"

    print("🧹 Cleaning up old deployment builds...")
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    print("🚀 Initiating recursive static assets transfer...")
    copy_directory_recursive(source_folder, destination_folder)

    # FIX: Swap out the single hardcoded file trigger for the dynamic directory crawler!
    print("🎨 Launching recursive multi-page compilation sequence...")
    generate_pages_recursive("content", "template.html", "public")
    print("🎉 All directory pages successfully generated and published!")


if __name__ == "__main__":
    main()
