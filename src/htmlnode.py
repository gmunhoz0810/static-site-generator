class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'

        return props_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes must have a value.")
        
        html_str = ""
        if self.tag:
            html_str += f"<{self.tag}"
            if self.props:
                html_str += f"{self.props_to_html()}"
            html_str += ">"

        html_str += self.value

        if self.tag:
            html_str += f"</{self.tag}>"

        return html_str
    
class ParentNode(HTMLNode):
    def __init__(self, children, tag, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag.")
        
        if not self.children:
            raise ValueError("Parent nodes must have a child.")
        
        html_str = ""
        if self.tag:
            html_str += f"<{self.tag}"
            if self.props:
                html_str += f"{self.props_to_html()}"
            html_str += ">"

        for child in self.children:
            html_str += child.to_html()

        if self.tag:
            html_str += f"</{self.tag}>"

        return html_str


