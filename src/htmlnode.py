import re
from enum import Enum
from textnode import (
    markdown_to_blocks,
    block_to_block_type,
    text_to_textnodes,
    BlockType,
    TextNode,
    TextType
)

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        attrs = ""
        if self.props:
            for prop, value in self.props.items():
                attrs += f' {prop}="{value}"'
        
        result = f"<{self.tag}{attrs}>"
        
        if self.value:
            result += self.value
        
        if self.children:
            for child in self.children:
                result += child.to_html()
        
        result += f"</{self.tag}>"
        return result
    
    def props_to_html(self):
        final_string = ""
        if self.props == None:
            return final_string
        else:
            for key in sorted(self.props.keys()):
                final_string += f' {key}="{self.props[key]}"'

            return final_string
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def __eq__(self, otherNode):
        if (self.tag == otherNode.tag and
            self.value == otherNode.value and
            self.children == otherNode.children and
            self.props == otherNode.props):
            return True
        else:
            return False
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
        self.props = props
        self.children = None
    
    def to_html(self):
        if self.value == None:
            raise ValueError('all leafnodes must have a value')
        
        if self.tag == None:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        
        if self.children == None:
            raise ValueError("no children")
        
        rest_html = ""

        for node in self.children:
            rest_html += f"{node.to_html()}"

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{rest_html}</{self.tag}>"
    
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
    
def check_heading_level(block):
    if block.startswith("######"):
        return "h6"
    elif block.startswith("#####"):
        return "h5"
    elif block.startswith("####"):
        return "h4"
    elif block.startswith("###"):
        return "h3"
    elif block.startswith("##"):
        return "h2"
    else:
        return "h1"
    
def block_type_to_tag(blocktype):
    match blocktype:
        case BlockType.heading:
            raise Exception("for headings use check_heading_level")
        
        case BlockType.code:
            return "code"
        
        case BlockType.quote:
            return "blockquote"
        
        case BlockType.unordered_list:
            return "ul"
        
        case BlockType.ordered_list:
            return "ol"
        
        case BlockType.paragraph:
            return "p"
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes

def create_blocknode(block, blocktype):
    if blocktype == BlockType.paragraph:
        node = HTMLNode("p", None, [], None)
        block_content = block.replace("\n", " ")
        node.children = text_to_children(block_content)
        return node

    elif blocktype == BlockType.heading:
        level = check_heading_level(block)
        node = HTMLNode(level, None, [], None)
        content = block.lstrip("#").lstrip()
        node.children = text_to_children(content)
        return node
    
    elif blocktype == BlockType.code:
        pre_node = HTMLNode("pre", None, [], None)
        code_node = HTMLNode("code", None, [], None)

        lines = block.split("\n")
        code_content = "\n".join(lines[1:-1]) + "\n"

        text_node = TextNode(code_content, TextType.TEXT)
        code_html_node = text_node_to_html_node(text_node)

        code_node.children = [code_html_node]
        pre_node.children = [code_node]
        return pre_node
    
    elif blocktype == BlockType.quote:
        content = "\n".join([line.lstrip(">").lstrip() for line in block.split("\n")])
        node = HTMLNode("blockquote", None, [], None)
        content = content.replace("\n", " ")
        node.children = text_to_children(content)
        return node
    
    elif blocktype == BlockType.unordered_list:
        ul_node = HTMLNode("ul", None, [], None)
        
        items = block.split("\n")
        for item in items:
            item_content = item.lstrip("- ").lstrip("* ").strip()
            if not item_content:
                continue
                
            li_node = HTMLNode("li", None, [], None)
            li_node.children = text_to_children(item_content)
            ul_node.children.append(li_node)
            
        return ul_node
        
    elif blocktype == BlockType.ordered_list:
        ol_node = HTMLNode("ol", None, [], None)
        
        items = block.split("\n")
        for item in items:
            item_parts = item.strip().split(". ", 1)
            if len(item_parts) < 2:
                continue
                
            item_content = item_parts[1].strip()
            if not item_content:
                continue
                
            li_node = HTMLNode("li", None, [], None)
            li_node.children = text_to_children(item_content)
            ol_node.children.append(li_node)
            
        return ol_node    

def markdown_to_html_node(markdown):
    div_node = HTMLNode("div", None, [], None)

    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        if not block.strip():
            continue

        block_type = block_to_block_type(block)
        block_node = create_blocknode(block, block_type)
        div_node.children.append(block_node)

    return div_node