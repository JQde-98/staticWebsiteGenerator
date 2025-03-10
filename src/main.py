import os 
import shutil
from htmlnode import markdown_to_html_node

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    os.mkdir(dest_dir)
    items = os.listdir(source_dir)

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            copy_static(source_path, dest_path)

def extract_title(markdown):
    if markdown.startswith("# "):
        split_markdown = markdown.split("\n") 
        main_heading = split_markdown[0]
        main_heading = main_heading.replace('#', '', 1)
        main_heading = main_heading.strip()
        return main_heading
    else:
        raise Exception("no heading detected")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()

    if not dest_path.endswith(".html"):
        dest_path = os.path.splitext(dest_path)[0] + ".html"

    try:
        htmlnode = markdown_to_html_node(markdown)
        html = htmlnode.to_html()
        html_heading = extract_title(markdown)
    except Exception as e:
        print(f"Error parsing Markdown file at {from_path}: {e}")
        print("Skipping this file.")
        return

    template = template.replace("{{ Title }}", html_heading)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    
    for item in dir_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            dest_file_path = os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html")
            generate_page(item_path, template_path, dest_file_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_dir_path)

    

def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()