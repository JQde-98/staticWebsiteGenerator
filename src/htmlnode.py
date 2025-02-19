class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
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