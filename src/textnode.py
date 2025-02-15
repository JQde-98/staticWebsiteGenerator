from enum import Enum

class TextType(Enum):
    NORMAL = 'normal'
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
    
