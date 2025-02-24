from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

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
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue    

        split_text = str(node.text).split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception('invalid Markdown syntax')
        
        for i in range(0, len(split_text)):
            if i == 0 or i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            elif i % 2 != 0:
                new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes