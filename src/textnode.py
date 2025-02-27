import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class BlockType(Enum):
    paragraph = 'paragraph'
    heading = 'heading'
    code = 'code'
    quote = 'quote'
    unordered_list = 'unordered_list'
    ordered_list = 'ordered_list'

class TextNode:
    def __init__(self, text, text_type, url=None): 
        self.text = text 
        self.text_type = text_type
        self.url = url 

    def __eq__(self, otherNode):
        if (self.text == otherNode.text and
            self.text_type == otherNode.text_type and
            self.url == otherNode.url):
            return True
        else:
            return False
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def __eq__(self, other_node):
        if not isinstance(other_node, TextNode):
            return False
        
        if self.url is not None and other_node.url is not None:
            return (self.text == other_node.text and 
                    self.text_type == other_node.text_type and 
                    self.url == other_node.url)
        
        return (self.text == other_node.text and 
                self.text_type == other_node.text_type)

    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception('invalid text type')
        
def extract_markdown_images(text):
    matched_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_text

def extract_markdown_links(text):
    matched_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_text
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue    

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception('invalid Markdown syntax')
        
        for i in range(0, len(split_text)):
            if (i == 0 or i % 2 == 0) and (split_text[i].strip() != ""):
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            elif i % 2 != 0:
                new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)

        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        else:
            image_alt, image_url = extracted_images[0]

            split_node = node.text.split(f"![{image_alt}]({image_url})", 1)
                
            if split_node[0].strip() != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if split_node[1] != "":
                image_check =  extract_markdown_images(split_node[1])
                if len(image_check) == 0:
                    new_nodes.append(TextNode(split_node[1], TextType.TEXT))
                elif split_node[1].strip() != "":
                    remaining_nodes = [TextNode(split_node[1], TextType.TEXT)]
                    rest_of_new_nodes = split_nodes_image(remaining_nodes)
                    if rest_of_new_nodes and len(rest_of_new_nodes) > 0:
                        new_nodes.extend(rest_of_new_nodes)

    return new_nodes
        


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)

        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        else:
            text, url = extracted_links[0]

            split_node = node.text.split(f"[{text}]({url})", 1)
                
            if split_node[0].strip() != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, url))

            if split_node[1] != "":
                link_check =  extract_markdown_links(split_node[1])
                if len(link_check) == 0:
                    new_nodes.append(TextNode(split_node[1], TextType.TEXT))
                elif split_node[1].strip() != "":
                    remaining_nodes = [TextNode(split_node[1], TextType.TEXT)]
                    rest_of_new_nodes = split_nodes_link(remaining_nodes)
                    if rest_of_new_nodes and len(rest_of_new_nodes) > 0:
                        new_nodes.extend(rest_of_new_nodes)

    return new_nodes

def text_to_textnodes(text):
    textnodes = []
    textnodes.append(TextNode(text, TextType.TEXT))

    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "*", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE) 
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)

    return textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    for block in blocks:
        stripped_block = block.replace("    ", "")
        stripped_block = stripped_block.strip()
        if len(stripped_block) == 0:
           blocks.remove(block) 
        elif len(stripped_block) != 0:
            blocks[blocks.index(block)] = stripped_block      

    return blocks
    
def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r'^#{1,6} ', block):
        return BlockType.heading
    
    if re.match(r'^```', block) and re.search(r'```$', block):
        return BlockType.code
    
    if all(line.startswith('>') for line in lines):
        return BlockType.quote
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.unordered_list
    
    if lines[0].startswith("1. "):
        is_ordered_list = True

        for i in range(len(lines)):
            expected_prefix = f"{i + 1}. "
            if not lines[i].startswith(expected_prefix):
                is_ordered_list = False
                break
        
        if is_ordered_list:
            return BlockType.ordered_list
        
    return BlockType.paragraph