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