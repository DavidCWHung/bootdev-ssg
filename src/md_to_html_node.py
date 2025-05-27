import os

from htmlnode import ParentNode

from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from utility import text_to_textnodes, extract_title
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    parent = ParentNode("div", [])
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line[2:])
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    li_html_nodes = []
    for line in lines:
        children = text_to_children(line[2:])
        li_html_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_html_nodes)

def olist_to_html_node(block):
    lines = block.split("\n")
    li_html_nodes = []
    for line in lines: 
        children = text_to_children(line[3:])
        li_html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_html_nodes)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}")
    with open(from_path, 'r') as f:
        read_data_from_path = f.read()
        
    
    with open(template_path, 'r') as f:
        read_data_template_path = f.read()

    md_html_node_string = markdown_to_html_node(read_data_from_path).to_html()

    h1 = extract_title(read_data_from_path)

    new_html = read_data_template_path.replace("{{ Title }}", h1).replace("{{ Content }}", md_html_node_string)

    with open(dest_path, 'w') as f:
        f.write(new_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(src_path):
            with open(src_path, 'r') as f:
                print(f"Reading data from {src_path}")
                read_data_src_path = f.read()

            with open(template_path, 'r') as f:
                print(f"Using template {template_path} to create html file...")
                read_date_template_path = f.read()

            md_html_node_string = markdown_to_html_node(read_data_src_path).to_html()

            h1 = extract_title(read_data_src_path)

            new_html_string = read_date_template_path.replace("{{ Title }}", h1).replace("{{ Content }}", md_html_node_string)

            with open(dest_path[:-2] + 'html', 'w') as f:
                f.write(new_html_string)
        else:
            os.mkdir(dest_path)
            print(f"Creating directory {dest_path}")
            generate_pages_recursive(src_path, template_path, dest_path)