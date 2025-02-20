import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode('this is a text node', TextType.ITALIC, "")
        node2 = TextNode('this is a test node', TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode('test test test', TextType.IMAGE, None)
        node2 = TextNode('test test test', TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
    
        html_node = text_node_to_html_node(text_node)
    
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_text2(self):
        text_node = TextNode("Hello, world!", TextType.BOLD)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)  

    def test_text_node_to_html_node_text3(self):
        text_node = TextNode("Hello, world!", TextType.ITALIC)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)    

    def test_text_node_to_html_node_text4(self):
        text_node = TextNode("Hello, world!", TextType.CODE)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)    

    def test_text_node_to_html_node_text5(self):
        text_node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    
        html_node = text_node_to_html_node(text_node)
    
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})           

    def test_text_node_to_html_node_text6(self):
        text_node = TextNode("My Cat", TextType.IMAGE, "https://cats.com/cat.png")
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://cats.com/cat.png", "alt": "My Cat"})  

    def test_text_node_to_html_node_exception(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        text_node.text_type = "invalid_type"
    
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()