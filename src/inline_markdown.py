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

def split_nodes_image(old_nodes):
    new_nodes = []

    if not old_nodes:
        return new_nodes

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue

        alt, link = images[0]
        image_text = f"![{alt}]({link})"
        sections = old_node.text.split(image_text, 1)

        if len(sections[0]) > 0:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(alt, TextType.IMAGE, link))

        if len(sections) > 1 and sections[1]:
            new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    if not old_nodes:
        return new_nodes

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        text, link = links[0]
        link_text = f"[{text}]({link})"
        sections = old_node.text.split(link_text, 1)

        if len(sections[0]) > 0:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(text, TextType.LINK, link))

        if len(sections) > 1:
            new_nodes.extend(split_nodes_link([TextNode(sections[1], TextType.TEXT)]))

    return new_nodes
