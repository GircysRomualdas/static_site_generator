import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        start_index = text.find(delimiter)

        if start_index == -1:
            new_nodes.append(old_node)
            continue 

        end_index = text.find(delimiter, start_index + len(delimiter))

        if end_index == -1:
            raise ValueError(f"No closing delimiter found for {delimiter}")
        if start_index > 0:
            new_nodes.append(TextNode(text[:start_index], TextType.TEXT))
        
        new_nodes.append(TextNode(text[start_index + len(delimiter): end_index], text_type))     
        end_text = text[end_index + len(delimiter):]

        if end_text:
            if delimiter not in end_text:
                new_nodes.append(TextNode(end_text, TextType.TEXT))
            else:
                new_nodes.extend(split_nodes_delimiter([TextNode(end_text, TextType.TEXT)], delimiter, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

