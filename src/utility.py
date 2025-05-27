import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        num_delimiter = old_node.text.count(delimiter)
        if num_delimiter % 2 != 0:
            raise Exception("invalid markdown syntax")
        
        new_parts = []
        parts = old_node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_part = TextNode(part, TextType.TEXT)
            else:
                new_part = TextNode(part, text_type)
            new_parts.append(new_part)
        if parts[-1] == "":
            new_parts.pop()

        new_nodes.extend(new_parts)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text_to_be_converted = old_node.text

        if len(extract_markdown_images(text_to_be_converted)) == 0:
            new_nodes.append(old_node)
            continue

        for image_alt, image_link in extract_markdown_images(text_to_be_converted):
            sections = text_to_be_converted.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_to_be_converted = sections[1]
            # to continue
        
        if text_to_be_converted != "":
            new_nodes.append(TextNode(text_to_be_converted, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text_to_be_converted = old_node.text
        if len(extract_markdown_links(text_to_be_converted)) == 0:
            new_nodes.append(old_node)
            continue

        for displayed_text, url in extract_markdown_links(text_to_be_converted):
            sections = text_to_be_converted.split(f"[{displayed_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(displayed_text, TextType.LINK, url))
            text_to_be_converted = sections[1]
        
        if text_to_be_converted != "":
            new_nodes.append(TextNode(text_to_be_converted, TextType.TEXT))
    
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    old_node = TextNode(text, TextType.TEXT)
    nodes_after_bold = split_nodes_delimiter([old_node], "**", TextType.BOLD)
    nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)
    nodes_after_code = split_nodes_delimiter(nodes_after_italic, "`", TextType.CODE)
    nodes_after_image = split_nodes_image(nodes_after_code)
    nodes_after_link = split_nodes_link(nodes_after_image)
    return nodes_after_link


def extract_title(markdown):
    h1 = ""
    for line in markdown.split('\n'):
        if line.startswith('# '):
            h1 = line[2:].strip()
            break
    
    if h1 == "":
        raise Exception("No h1 header")

    return h1


